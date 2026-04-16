# ruff: noqa: S101, D103

"""Tests für PUT."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import put
from pytest import mark

POSITION_UPDATE: Final = "T"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    fussballer_id: Final = 40
    if_match: Final = '"0"'
    geaenderter_fussballer: Final = {
        "nachname": "Mockput",
        "nationalitaet": "Deutschland",
        "position": POSITION_UPDATE,
        "geburtsdatum": "2022-06-01",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match
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
    fussballer_id: Final = 40
    geaenderter_fussballer_invalid: Final = {
        "nachname": "1falschernachname123",
        "nationalitaet": "Deutschland",
        "position": "POSITION_UPDATE",
        "geburtsdatum": "2022-02-01",
        "username": "testrestinvalid",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "If-Match": '"0"',
        "Authorization": f"Bearer {token}"
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
    assert "nachname" in body


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    fussballer_id: Final = 999999
    if_match: Final = '"0"'
    geaenderter_fussballer: Final = {
        "nachname": "Mockput",
        "nationalitaet": "Deutschland",
        "position": POSITION_UPDATE,
        "geburtsdatum": "2022-02-01",
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
def test_put_alte_version() -> None:
    # arrange
    fussballer_id: Final = 40
    if_match: Final = '"-1"'
    geaenderter_fussbller: Final = {
        "nachname": "Mockput",
        "nationalitaet": "Deutschland",
        "position": POSITION_UPDATE,
        "geburtsdatum": "2022-02-01",
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
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
