from dataclasses import asdict
from typing import TYPE_CHECKING

from pytest import fixture, mark, raises

from fussballer.entity import Adresse, Fussballer, Position
from fussballer.security import Role, User
from fussballer.service import ForbiddenError, NotFoundError, FussballerDto, FussballerService

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    mocker.patch(
        "fussballer.service.fussballer_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, exc_type, exc, tb: None,
        ),
    )
    return session


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_success(fussballer_service: FussballerService, session_mock) -> None:
    """Szenario 1: Erfolgreiches Abrufen des eigenen Profils."""
    fussballer_id = 1
    username = "mocktest"

    user_mock = User(username, email="mock@test.de", nachname="Mock", vorname="", roles=[Role.FUSSBALLER], password="p")
    fussballer_mock = Fussballer(
        id=fussballer_id, name="Mocktest", nationalitaet="DE", position=Position.STUERMER,
        username=username, email="mock@test.de", adresse=None, auszeichnungen=[]
    )

    session_mock.scaler.return_value = fussballer_mock
    assert asdict(fussballer_dto) == asdict(FussballerDTO(fussballer_mock))


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_not_found(fussballer_service:
