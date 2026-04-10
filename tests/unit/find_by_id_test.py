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
def test_find_by_id_not_found(fussballer_service: FussballerService, session_mock) -> None:
    """Szenario 2: Fussballer existiert nicht in der Datenbank."""
    fussballer_id = 999
    user_mock = User("mocktest", "mock@test.de", "Mock",
                     vorname="", roles=[Role.ADMIN], password="p")

    session_mock.scalar.return_value = None

    with raises(NotFoundError) as err:
        fussballer_service.find_by_id(fusballer_id=fussballer_id, user=user_mock)
    assert err.value.fussballer_id == fussballer_id


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_forbidden(fussballer_service: FussballerService, session_mock) -> None:
    """Szenario 3: Zugriff auf fremdes Profil wird verweigert."""
    fussballer_id = 1

    # User heißt "other", Fussballer gehört aber "mocktest"
    user_mock = User(username="other", email="other@test.de", nachname="Other", vorname="", roles=[Role.FUSSBALLER], password="p")
    fussballer_mock = Fussballer(
        id=fussballer_id, name="Mocktest", nationalitaet="DE", position=Position.STUERMER,
        username="mocktest", email="mock@test.de", adresse=None, auszeichnungen=[]
    )

    session_mock.scalar.return_value = fussballer_mock

    with raises(ForbiddenError) as err:
        fussballer_service.find_by_id(fussballer_id=fussballer_id, user=user_mock)
    assert err.type == ForbiddenError
