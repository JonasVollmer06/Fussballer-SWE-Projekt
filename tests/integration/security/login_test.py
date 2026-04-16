# ruff: noqa: S101, D103
"""Tests für Login."""

from http import HTTPStatus
from typing import Final

from common_test import (
    base_url,
    ctx,
    login,
    timeout,
    token_path,
    username_admin,
)
from httpx import post
from pytest import mark


@mark.login
def test_login_admin() -> None:
    # act
    token: Final = login()

    # assert
    assert isinstance(token, str)
    assert token


@mark.login
def test_login_falsches_passwort() -> None:
    # arrange
    login_data: Final = {"username": username_admin, "password": "FALSCHES_PASSWORT"}

    # act
    response: Final = post(
        url=f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.login
def test_login_unbekannter_user() -> None:
    # arrange
    login_data: Final = {"username": "GIBTS_NICHT", "password": "IRGENDEIN_PASSWORT"}

    # act
    response: Final = post(
        url=f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
