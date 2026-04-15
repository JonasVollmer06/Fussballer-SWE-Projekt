"""Mögliche Ausnahmen in der Geschäftslogig."""

from collections.abc import Mapping

__all__ = [
    "ForbiddenError",
    "NotFoundError",
    "UsernameExistsError",
    "VersionOutdatedError",
    ]


class ForbiddenError(Exception):
    """Eine Ausnahme wenn der Zugriff abgelehnt wird."""


class UsernameExistsError(Exception):
    """Exception, falls der Benutzername bereits existiert."""

    def __init__(self, username: str | None) -> None:
        """Initialisierung von UsernameExistsError mit dem Benutzernamen.

        :param username: Bereits existierender Benutzername
        """
        super().__init__(f"Existierender Benutzername: {username}")
        self.username = username


class NotFoundError(Exception):
    """Eine Ausnahme wenn kein passendes Fussballer-Objekt gefunden wurde."""

    def __init__(
        self,
        fussballer_id: int | None = None,
        suchparameter: Mapping[str, str] | None = None,
    ) -> None:
        """Definition der NotFoundError Exception."""
        super().__init__("Not Found")
        self.fussballer_id = fussballer_id
        self.suchparameter = suchparameter


class VersionOutdatedError(Exception):
    """Exception, falls die Versionsnummer beim Aktualisieren veraltet ist."""

    def __init__(self, version: int) -> None:
        """Initialisierung von VersionOutdatedError mit veralteter Versionsnummer.

        :param version: Veraltete Versionsnummer
        """
        super().__init__(f"Veraltete Version: {version}")
        self.version = version
