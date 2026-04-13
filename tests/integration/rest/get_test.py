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


@mark.rest
@mark.get_request
@mark.parametrize("teil", ["Mock", "test"])
def test_get_by_nachname(teil : str) -> None:
    # arrange
    params = {"nachname": teil}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body["content"]

    for f in content:
        nachname = f.get("nachname")
        assert nachname is not None and isinstance(nachname, str)
        assert teil.lower() in nachname.lower()
        assert f.get("id") is not None



@mark.rest
@mark.get_request
@mark.parametrize("nachname", ["GibtEsNicht", "Foo_bar"])
def test_get_by_nachname_not_found(nachname: str) -> None:
    # arrange
    params = {"nachname": nachname}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    #assert
    assert response.status_code == HTTPStatus.NOT_FOUND



@mark.rest
@mark.get_request
@mark.parametrize("teil", ["a", "n"])
def test_get_nachnamen(teil: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/nachnamen/{teil}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    nachnamen: Final = response.json()
    assert isinstance(nachnamen, list)
    assert len(nachnamen) > 0

    for nachname in nachnamen:
        assert teil in nachname.lower()
