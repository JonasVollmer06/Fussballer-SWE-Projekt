"""Tests für GET mit Query-Parameter."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
@mark.parametrize("email", ["spieler1@test.de", "mock@test.de"])
def test_get_by_email(email: str) -> None:
    # arrange
    params = {"email": email}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        rest_url,
        params=params,
        headers=headers,
        verify=ctx
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    content: Final = response_body["content"]

    assert isinstance(content, list)
    assert len(content) == 1

    fussballer = content[0]
    assert fussballer is not None
    assert fussballer.get("email") == email
    assert fussballer.get("id") is not None


@mark.rest
@mark.get_request
@mark.parametrize("email", ["gibt.es.nicht@test.com", "nobody@acme.de"])
def test_get_by_email_not_found(email: str) -> None:
    # arrange
    params = {"email": email}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        rest_url,
        params=params,
        headers=headers,
        verify=ctx
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND
