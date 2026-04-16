"""Modul für die GraphQL-Schnittstelle."""

from collections.abc import Sequence

from fussballer.graphql_api.graphql_types import (
    AdresseInput,
    AuszeichnungInput,
    CreatePayload,
    FussballerInput,
)
from fussballer.graphql_api.schema import Mutation, Query, graphql_router

__all__: Sequence[str] = [
    "AdresseInput",
    "AuszeichnungInput",
    "CreatePayload",
    "FussballerInput",
    "Mutation",
    "Query",
    "graphql_router",
]
