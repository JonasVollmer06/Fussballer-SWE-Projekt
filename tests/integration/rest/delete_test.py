"""Tests für DELETE."""

from typing import Final

from common_test import ctx, login, rest_url
from httpx import delete
from pytest import mark


@mark.rest
@mark.delete_request
def test_delete() -> None:
    # arrange
    fussballer_id: Final = 60
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = delete(
        url=f"{rest_url}/{fussballer_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == 204


@mark.rest
@mark.delete_request
def test_delete_not_found() -> None:
    # arrange
    fussballer_id: Final = 999999
    token: Final = login()
    assert token is not None
    headers: dict[str, str] = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = delete(
        url=f"{rest_url}/{fussballer_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == 204
