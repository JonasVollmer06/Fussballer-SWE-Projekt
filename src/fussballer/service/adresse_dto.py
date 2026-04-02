"""DTO-Klasse für die Adresse, ohne Decorators, für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

from fussballer.entity import Adresse


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class AdresseDTO:
    """DTO-Klasse für die Adresse, ohne Decorators, für SQLAlchemy."""

    plz: str
    ort: str
    bundesland: str

    def __init__(self, adresse: Adresse) -> None:
        """Initialisierung von AdresseDTO durch ein Entity-Objekt von Adresse.

        :param adresse: Adresse-Objekt mit Decorators für SQLAlchemy
        """
        self.plz: str = adresse.plz
        self.ort: str = adresse.ort
        self.bundesland: str = adresse.bundesland
