"""Enum für die Fussballer Hauptposition."""

from enum import StrEnum

import strawberry


@strawberry.enum
class Position(StrEnum):
    """Enum für die Fussballer Hauptposition."""

    TORWART = "T"
    """Torwart."""

    VERTEIDIGER = "V"
    """Verteidiger."""

    MITTELFELDSPIELER = "M"
    """Mittelfeldspieler."""

    STUERMER = "S"
    """Stürmer."""
