"""Container der Objekte fürs Paging."""

from dataclasses import dataclass
from typing import TypeVar

__all__ = ["Slice"]

T = TypeVar("T")


@dataclass(eq=False, slots=True, kw_only=True)
class Slice[T]:
    """Dataclass für gefundene Objekte im Kontext Paging."""

    content: tuple[T, ...]
    """Objekte einer Seite des Paging."""

    total_elements: int
    """Gesamtanzahl der gefundenen Elemente."""
