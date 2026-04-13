"""Type Definition für das GraphQL-Schema mit Strawberry."""

from datetime import date

import strawberry

from fussballer.entity import Position

__all__ = [
    "AdresseInput",
    "AuszeichnungInput",
    "CreatePayload",
    "FussballerInput"
]


@strawberry.input
class AdresseInput:
    """Input-Klasse für einen Fussballer mit GraphQL und Strawberry."""

    plz: str

    ort: str

    bundesland: str


@strawberry.input
class AuszeichnungInput:
    """Input-Klasse für einen Fussballer mit GraphQL und Strawberry."""

    bezeichnung: str

    saison: str


@strawberry.input
class FussballerInput:
    """Input-Klasse für einen Fussballer mit GraphQL und Strawberry."""

    nachname: str

    position: Position

    geburtsdatum: date

    nationalitaet: str

    username: str

    adresse: AdresseInput

    auszeichnungen: list[AuszeichnungInput]


@strawberry.type
class CreatePayload:
    """RückgabeTyp für die ID, welche beim anlegen zurückgeschickt wird."""

    id: int
