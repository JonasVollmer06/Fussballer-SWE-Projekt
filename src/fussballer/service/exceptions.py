"""Mögliche Ausnahmen in der Geschäftslogig."""

from collections.abc import Mapping

__all__ = [
    "ForbiddenError",
    "NotFoundError",
    ]


class ForbiddenError(Exception):
    """Eine Ausnahme wenn der Zugriff abgelehnt wird."""


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
