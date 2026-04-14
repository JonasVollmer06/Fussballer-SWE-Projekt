"""Tests für PUT."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import put
from pytest import mark

USERNAME_UPDATE: Final = "username_put"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    fussballer_id: Final = 1
    if_match: Final = '"0"'
    geaenderter_fussballer: Final = {
        "nachname": "Mockput",
        "nationalitaet": "DE",
        "position": "MITTELFELD",
        "username": USERNAME_UPDATE,
        "adresse": {"plz": "99999", "ort": "Restort", "bundesland": "Restland"},
        "auszeichnungen": []
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{fussballer_id}",
        json=geaenderter_fussballer,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text
