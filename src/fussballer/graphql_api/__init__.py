"""Modul für die GraphQL-Schnittstelle."""

from collections.abc import Sequence

from fussballer.graphql_api import graphql_router

__all__: Sequence[str] = [
    "graphql_router",
    "CreatePayload",
    "Mutation",
    "Query",
    "AuszeichnungInput",
    ""
]
