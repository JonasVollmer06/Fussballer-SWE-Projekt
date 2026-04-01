"""Datei zum Definieren der Parameter für Pagination."""

from dataclasses import dataclass
from typing import Final

__all__ = ["Pageable"]

DEFAULT_PAGE_SIZE = 5
MAX_PAGE_SIZE = 100
DEFALT_PAGE_NUMBER = 0


@dataclass(eq=False, slots=True, kw_only=True)
class Pageable:
    """Dataclass für die Definition der Parameter für Pagination."""

    size: int
    """Angeforderte Datensätze pro Seite."""

    number: int
    """Angeforderte Seitenzahl."""

    @staticmethod
    def create(number: str | None = None, size: str | None = None) -> Pageable:
        """Objekt fürs Paging aus gegebenen Daten erzeugen."""
        number_int: Final = (
            DEFALT_PAGE_NUMBER
            if number is None or not number.isdigit()
            else int(number)
        )
        size_int: Final = (
            DEFAULT_PAGE_SIZE
            if size is None
            or not size.isdigit()
            or int(size) > MAX_PAGE_SIZE
            or int(size) < 0
            else int(size)
        )
        return Pageable(size=size_int, number=number_int)
