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
        "position": "MITTELFELDSPIELER",
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


@mark.rest
@mark.put_request
def test_put_invalid() -> None:
    # arrange
    fussballer_id: Final = 1
    geaenderter_fussballer_invalid: Final = {
        "nachname": "falscher_nachname_123",
        "nationalitaet": "Deutschland",
        "position": "FALSCHE_POSITION",
        "username": "testrestinvalid",
        "adresse": {"plz": "12", "ort": "Restort", "bundesland": "Restland"},
        "auszeichnungen": []
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": '"0"',
    }

    # act
    response: Final = put(
        f"{rest_url}/{fussballer_id}",
        json=geaenderter_fussballer_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.text
    assert "position" in body
    assert "plz" in body


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    fussballer_id: Final = 999999
    if_match: Final = '"0"'
    geaenderter_fussballer: Final = {
        "nachname": "Mockput",
        "nationalitaet": "DE",
        "position": "MITTELFELDSPIELER",
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
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_username_exists() -> None:
    # arrange
    fussballer_id: Final = 1
    if_match: Final = '"0"'
    username_exists: Final = "admin_user"
    geaenderter_fussbller: Final = {
        "nachname": "Mockput",
        "nationalitaet": "DE",
        "position": "MITTELFELDSPIELER",
        "username": username_exists,
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
        json=geaenderter_fussbller,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert username_exists in response.text
