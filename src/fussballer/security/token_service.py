"""Service für die Authentifizierung und Token erstellung mit Keycloak."""
from collections.abc import Mapping
from dataclasses import asdict
from typing import Any, Final

from fastapi import Request
from jwcrypto.common import JWException
from keycloak import KeycloakAuthenticationError, KeycloakOpenID

from fussballer.config import keycloak_config
from fussballer.security.exceptions import AuthorizationError, LoginError
from fussballer.security.role import Role
from fussballer.security.user import User

__all__ = ["TokenService"]


class TokenService:
    """Service-Klasse für die Authentifizierung und Verarbeitung von Tokens."""

    def __init__(self) -> None:
        """Kontruktor des TokenService."""
        self.keycloak = KeycloakOpenID(**asdict(keycloak_config))

    def token(self, username: str | None, password: str | None) -> Mapping[str, str]:
        """Passenden Access- und Refresh-Token zu Benutzername und Passwort finden.

        :return: Access- und Refresh-Token
        """
        if username is None or password is None:
            raise LoginError(username=username)

        try:
            token = self.keycloak.token(username, password)
        except KeycloakAuthenticationError:
            raise LoginError(username=username) from KeycloakAuthenticationError

        return token

    def _get_token_from_request(self, request: Request) -> str:
        """Token aus Request-Header holen.

        :return: Extrahierter Bearer-Token
        """
        authorization_header: Final = request.headers.get("Authorization")

        if authorization_header is None:
            raise AuthorizationError

        try:
            authorization_scheme, bearer_token = authorization_header.split()
        except ValueError:
            raise AuthorizationError from ValueError

        if authorization_scheme.lower() != "bearer":
            raise AuthorizationError

        return bearer_token

    def get_user_from_token(self, token: str) -> User:
        """Benötigte Daten des Benutzters aus Token holen.

        :return: Benötigte Daten
        """
        try:
            token_decoded: Final = self.keycloak.decode_token(token=token)
        except JWException:
            raise AuthorizationError from JWException

        username: Final[str] = token_decoded["preferred_username"]
        email: Final[str] = token_decoded["email"]
        nachname: Final[str] = token_decoded["family_name"]
        vorname: Final[str] = token_decoded["given_name"]
        roles = self.get_roles_from_token(token_decoded)

        return User(
            username=username,
            email=email,
            nachname=nachname,
            vorname=vorname,
            roles=roles,
        )

    def get_user_from_request(self, request: Request) -> User:
        """Holt den Token aus dem Request-Header und extrahiert daraus die User-Daten.

        :return: Rückgabe der User-Daten
        """
        bearer_token: Final = self._get_token_from_request(request)
        user: Final = self.get_user_from_token(token=bearer_token)

        return user

    def get_roles_from_token(self, token: str | Mapping[str, Any]) -> list[Role]:
        """Rollen aus Access-Token extrahieren.

        :return: Eine Liste mit extrahierten Rollen
        """
        if isinstance(token, str):
            token_decoded = self.keycloak.decode_token(token=token)
        else:
            token_decoded = token

        roles: Final[str] = token_decoded["resource_access"][self.keycloak.client_id][
            "roles"
        ]

        roles_enum: Final = [Role[role.upper()] for role in roles]

        return roles_enum
