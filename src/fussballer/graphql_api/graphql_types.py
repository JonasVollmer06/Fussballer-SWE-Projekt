"""Type Definition für das GraphQL-Schema mit Strawberry."""

from datetime import date

import strawberry

from fussballer.entity import Position

__all__ = [
    "AdresseInput",
    "AuszeichnungInput",
    "CreatePayload",
    "LoginPayload",
    "SuchparameterInput",
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


@strawberry.input
class SuchparameterInput:
    """Input-Klasse für GraphQL-Suchparameter."""

    nachname: str | None = None


@strawberry.type
class CreatePayload:
    """RückgabeTyp für die ID, welche beim anlegen zurückgeschickt wird."""

    id: int


@strawberry.type
class LoginPayload:
    """RückgabeTyp für den GraphQL-Login."""

    token: str
