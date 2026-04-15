# ruff: noqa: S101, D103
"""Test für POST."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, rest_url
from httpx import post
from pytest import mark

token: str | None


@mark.rest
@mark.post_request
def test_post() -> None:
    # arrange
    neuer_fussballer: Final = {
        "nachname": "TestFussballer",
        "nationalitaet": "DE",
        "position": "STUERMER",
        "geburtsdatum": "2022-02-01",
        "username": "neu_rest",
        "adresse": {
            "plz": "99999",
            "ort": "Testort",
            "bundesland": "Testland"
            },
        "auszeichnungen": []
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_fussballer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neuer_fussballer_invalid: Final = {
        "nachname": "falscher_nachname_123",
        "nationalitaet": "DE",
        "position": "FALSCHE_POSITION",
        "geburtsdatum": "2022-02-01",
        "username": "testrestinvalid",
        "adresse": {"plz": "1234", "ort": "Restort", "bundesland": "Restland"},
        "auszeichnungen": []
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_fussballer_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.text
    assert "position" in body
    assert "plz" in body


@mark.rest
@mark.post_request
def test_post_username_exists() -> None:
    # arrange
    username_exists: Final = "jonas"
    neuer_fussballer: Final = {
        "nachname": "NachnameExists",
        "nationalitaet": "DE",
        "position": "TORWART",
        "geburtsdatum": "2022-02-01",
        "username": username_exists,
        "adresse": {"plz": "99999", "ort": "Restort", "bundesland": "Restland"},
        "auszeichnungen": []
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_fussballer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert username_exists in response.text
