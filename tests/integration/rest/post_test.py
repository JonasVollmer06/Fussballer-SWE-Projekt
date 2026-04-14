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
        "nachname": "NeuerRest",
        "nationalitaet": "DE",
        "position": "STUERMER",
        "username": "neu_rest",
        "adresse": {
            "plz": "99999",
            "ort": "Restort",
            "bundesland": "Restland"
            },
        "auszeichnungen": []
    }
    headers = {"Content_Type": "application/json"}

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
