"""DTO-Klasse für die Daten eines Fussballers, ohne Decorators, für SQLAlchemy."""

from dataclasses import dataclass
from datetime import date

import strawberry

from fussballer.entity import Position, Fussballer
from fussballer.service.adresse_dto import AdresseDTO

__all__: list[str] = ["FussballerDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class FussballerDTO:
    """DTO-Klasse für die Daten von ausgelesenen oder gespeicherten Fussballern, ohne Deorators."""

    id: int
    version: int
    nachname: str
    position: Position | None
    geburtsdstum: date
    nationalitaet: str

    def __init__(self, fussballer: Fussballer):
        """Initialisierung von FussballerDTO durch ein Entity-Objekt von Fussballer.

        :param fussballer: Fussballer-Objekt mit Decorators zu SQLAlchemy
        """
        fussballer_id: int | None = fussballer.id
        self.id: int = fussballer_id if fussballer_id is not None else -1
        self.version: int = fussballer.version
        self.nachname: str = fussballer.nachname
        self.position: Position | None = fussballer.position
        self.geburtsdstum: date = fussballer.geburtsdatum
        self.nationalitaet: str = fussballer.nationalitaet
