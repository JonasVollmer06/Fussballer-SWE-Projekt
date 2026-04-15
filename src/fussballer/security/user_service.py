"""Geschäftslogik zur Verwaltung der Benutzer mit Keycloak."""

from dataclasses import asdict
from typing import Any, Final, cast

from keycloak import KeycloakAdmin, KeycloakConnectionError
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from fussballer.config import keycloak_admin_config
from fussballer.security.role import Role
from fussballer.security.user import User

__all__ = ["UserService"]


class UserService:
    """Service-Klasse zum Mangement von Keycloak Nutzerdaten."""

    def __init__(self) -> None:
        """Konstruktor des UserServices."""
        self.keycloak_admin = KeycloakAdmin(**asdict(keycloak_admin_config))
        disable_warnings(InsecureRequestWarning)

        try:
            self.client_uuid: str = cast(
                "str",
                self.keycloak_admin.get_client_id(keycloak_admin_config.client_id),
            )
            roles = self.keycloak_admin.get_client_roles(client_id=self.client_uuid)
            roles_fussballer = [role for role in roles if role["name"] == "fussballer"]
            roles_admin = [role for role in roles if role["name"] == "admin"]
            self.rolle_fussballer = roles_fussballer[0]
            self.rolle_admin = roles_admin[0] if roles_admin else None
        except KeycloakConnectionError:
            self.client_uuid = "N/A"
            self.rolle_fussballer = None
            self.rolle_admin = None

    def username_exists(self, username: str) -> bool:
        """Methode zum überprüfen ob ein Benutzername existiert.

        :return: True, wenn übergebener Username exisitiert und False wenn nicht
        """
        user_id: Final = self.keycloak_admin.get_user_id(username)
        exists: Final = user_id is not None

        return exists

    def email_exists(self, email: str) -> bool:
        """Methode zum überprüfen ob eine Email existiert.

        :return: True, wenn übergebene Email exisitiert und False wenn nicht
        """
        users: Final = self.keycloak_admin.get_users(query={"email": email})
        exists: Final = len(users) > 0
        return exists

    def create_user(self, user: User) -> str:
        """Neuer Benutzer in Keycloak anlegen.

        :return: ID des in Keycloak angelegten Benutzers.
        """
        user_id: Final = self.keycloak_admin.create_user(
            payload={
                "username": user.username,
                "email": user.email,
                "lastName": user.nachname,
                "firstName": user.vorname,
                "credentials": [{"value": user.password, "type": "password"}],
                "enabled": True,
            },
            exist_ok=False,
        )
        client_roles = []
        if Role.ADMIN in user.roles and self.rolle_admin is not None:
            client_roles.append(self.rolle_admin)
        if Role.FUSSBALLER in user.roles and self.rolle_fussballer is not None:
            client_roles.append(self.rolle_fussballer)

        if client_roles:
            self.keycloak_admin.assign_client_role(
                user_id=user_id,
                client_id=self.client_uuid,
                roles=client_roles,
            )
        return user_id

    def remove_all_users(self) -> None:
        """Löschen aller nicht administratoren Keycloak Benutzer."""
        kc_users: Final = self.keycloak_admin.get_users()

        for kc_user in kc_users:
            if kc_user.get("username") == "admin":
                continue

            self.keycloak_admin.delete_user(kc_user.get("id"))

    def find_user_by_username(self, username: str) -> User | None:
        """Findet einen Benutzer anhand eines übergebenen Username.

        :return: Gefundener Benutzer
        """
        kc_users: Final = self.keycloak_admin.get_users({"username": username})
        if not kc_users:
            return None

        kc_user: Final = kc_users[0]
        kc_roles: Final[Any] = self.keycloak_admin.get_all_roles_of_user(kc_user["id"])
        kc_client_roles = kc_roles["clientMappings"][keycloak_admin_config.client_id][
            "mappings"
        ]

        roles: Final = [Role[role["name"].upper()] for role in kc_client_roles]
        user: Final = User(
            username=kc_user["username"],
            email=kc_user["email"],
            nachname=kc_user["lastName"],
            vorname=kc_user["firstName"],
            roles=roles,
        )

        return user
