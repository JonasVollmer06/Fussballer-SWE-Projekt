# ruff: noqa: S101, D103
"""Tests für Mutations mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url
from httpx import post
from pytest import mark


@mark.graphql
@mark.mutation
def test_create() -> None:
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    fussballerInput: {
                        nachname: "Nachnamegraphql"
                        position: STUERMER
                        geburtsdatum: "2004-08-16"
                        nationalitaet: "Deutschland"
                        adresse: {
                            plz: "99999"
                            ort: "Mutationort"
                            bundesland: "Mutationland"
                        }
                        auszeichnungen: [
                            {
                                bezeichnung: "POTY"
                                saison: "2024/25"
                            }
                        ]
                        username: "testgraphql"
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response is not None
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert isinstance(response_body["data"]["create"]["id"], int)
    assert response_body.get("errors") is None


@mark.graphql
@mark.mutation
def test_create_invalid() -> None:
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    fussballerInput: {
                        nachname: "falscher-name"
                        position: STUERMER
                        geburtsdatum: "2004-08-16"
                        nationalitaet: "@gibt-nicht123"
                        adresse: {
                            plz: "999"
                            ort: "Mutationort"
                            bundesland: "Mutationland"
                        }
                        auszeichnungen: [
                            {
                                bezeichnung: "POTY"
                                saison: "2024.25"
                            }
                        ]
                        username: "testgraphql"
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"] is None
    errors: Final = response_body["errors"]
    assert isinstance(errors, list)
    assert len(errors) == 1
