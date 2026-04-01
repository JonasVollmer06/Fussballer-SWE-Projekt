"""Geschäftslogik zum Lesen von Fussballer-Daten."""


__all__: list[str] = ["FussballerService"]


class FussballerService:
    """Service-Klasse mit Geschäftslogik für Fussballer."""

    def __init__(self, repo: FussballerRepository) -> None:
        """Konstruktor mit abhängigem FussballerRepository."""
        self.repo: FussballerRepository = repo
