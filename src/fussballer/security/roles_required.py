"""Klasse zur Überprüfung der Verfügbarkeit der Rollen."""

from typing import TYPE_CHECKING, Annotated, Final

from fastapi import Depends, HTTPException, Request, status
from loguru import logger

from fussballer.security.dependencies import get_token_service
from fussballer.security.role import Role
from fussballer.security .token_service import TokenService

if TYPE_CHECKING:
    from fussballer.security.user import User

__all__ = ["RolesRequired"]


class RolesRequired:
    """Überprüfung der erforderlichen Rollen."""

    def __init__(self, required_roles: list[Role] | Role) -> None:
        """Konstruktor der RolesRequired-Klasse."""
        self.required_roles = required_roles

    def __call__(
        self,
        request: Request,
        service: Annotated[TokenService, Depends(get_token_service)],
    ) -> None:
        """Überprüfung Verfügbarkeit des aktuellen Users."""
        user: Final[User] = service.get_user_from_request(request)

        if isinstance(self.required_roles, Role):
            if self.required_roles not in user.roles:
                logger.warning("Der Benutzer {} hat nicht die Rolle: {}", user,
                self.required_roles)
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            request.state.current_user = user
            return

        for role in user.roles:
            if role in self.required_roles:
                request.state.current_user = user
                return
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
