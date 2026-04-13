"""Type Definition für das GraphQL-Schema mit Strawberry."""

from datetime import date
from decimal import Decimal

import strawberry

import fussballer.entity import Position

__all__ = [
    "CreatePayload",
    "FussballerInput",
    "AdresseInput",
    "AuszeichnungInput"
]