"""Definierend er Parameter für Pagination."""

from dataclasses import dataclass
from math import ceil
from typing import Any, Final

from fussballer.repository import Pageable

__all__ = ["Page"]


@dataclass(eq=False, slots=True, kw_only=True)
class PageMeta:
    """Dataclass mit Metainformationen einer Page."""

    size: int
    """Anz. der Datensätze pro Seite."""

    number: int
    """Seitenzahl."""

    total_elements: int
    """Gesamtanzahl an Datensätzen."""

    total_pages: int
    """Gesamtanzahl an Seiten."""


@dataclass(eq=False, slots=True, kw_only=True)
class Page:
    """Dataclass mit den Seiten der gefundenen Datensätzen."""

    content: tuple[dict[str, Any], ...]
    """Gefunden Datensätze einer Seite in einem Tuple also unveränderliche
    Liste gespeicher.
    """

    page: PageMeta  # NOSONAR
    """Metadaten einer Seite."""

    @staticmethod
    def create(
        content: tuple[dict[str, Any], ...], pageable: Pageable, total_elements: int
    ) -> Page:
        """Erstellen einer Seite mit ihren Daten + Metainformationen."""
        total_pages: Final = ceil(total_elements / pageable.size)
        page_meta = PageMeta(
            size=pageable.size,
            number=pageable.number,
            total_elements=total_elements,
            total_pages=total_pages,
        )
        return Page(content=content, page=page_meta)
