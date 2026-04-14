"""Tests für GET mit Pfadparameter für die ID."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
@mark.parametrize("fussballer_id", [30, 2, 20])
def test_get_by_id_admin(fussballer_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{fussballer_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == fussballer_id


@mark.rest
@mark.get_request
def test_get_by_id_not_found() -> None:
    # arrange
    fussballer_id: Final = 999999
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{fussballer_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_by_id_fussballer() -> None:
    # arrange
    fussballer_id: Final = 20
    token: Final = login(username="mocktest")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{fussballer_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == fussballer_id


@mark.rest
@mark.get_request
@mark.parametrize("fussballer_id", [1, 30])
def test_get_by_id_not_allowed(fussballer_id: int) -> None:
    # arrange
    token: Final = login(username="mocktest")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{fussballer_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.FORBIDDEN


@mark.rest
@mark.get_request
def test_get_by_id_invalid_type() -> None:
    # arrange
    invalid_id = "abc"
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{invalid_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
