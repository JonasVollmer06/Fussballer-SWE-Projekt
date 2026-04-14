"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login_graphql
from httpx import post
from pytest import mark

GRAPHQL_PATH: Final = "/graphql"


@mark.graphql
@mark.query
def test_query_id() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}
    query: Final = {
        "query": """
            {
                fussballer(fussballerId: "1") {
                    version
                    nachname
                    nationalitaet
                    position
                    geburtsdatum
                    username
                    adresse {
                        plz
                        ort
                        bundesland
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(url=graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    data: Final = response_body["data"]
    assert data is not None
    fussballer: Final = data["fussballer"]
    assert isinstance(fussballer, dict)
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_id_not_found() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                fussballer(fussballerId: "999999") {
                    nachname
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"]["fussballer"] is None
    assert response_body.get("errors") is None
