# ruff: noqa: S101, S106, D103, ARG005
"""Unit-Tests für find_by_id() von FussballerService."""

from dataclasses import asdict

from pytest import fixture, mark, raises
from pytest_mock import MockerFixture

from fussballer.entity import Adresse, Fussballer, Position
from fussballer.security import Role, User
from fussballer.service import ForbiddenError, NotFoundError, FussballerDTO, FussballerService


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
def test_find_by_id_admin_success(
    fussballer_service: FussballerService, session_mock
) -> None:
    # Arrange
    fussballer_id = 1
    username_admin = "admin_user"
    username_spieler = "spieler_test"

    user_mock = User(
        username=username_admin,
        email="admin@test.de",
        nachname="Admin",
        vorname="Admin",
        roles=[Role.ADMIN],
        password="p"
    )

    adresse_mock = Adresse(
        id=11,
        plz="12345",
        ort="Mockort",
        bundesland="Mockland",
        fussballer_id=fussballer_id,
        fussballer=None,
    )

    fussballer_mock = Fussballer(
        id=fussballer_id,
        nachname="Spieler",
        nationalitaet="DE",
        position=Position.STUERMER,
        username=username_spieler,
        adresse=adresse_mock,
        auszeichnungen=[]
    )
    adresse_mock.fussballer = fussballer_mock
    fussballer_dto_mock = FussballerDTO(fussballer=fussballer_mock)

    session_mock.scalar.return_value = fussballer_mock

    # Act
    fussballer_dto = fussballer_service.find_by_id(
        fussballer_id=fussballer_id, user=user_mock
    )

    # Assert
    assert asdict(fussballer_dto) == asdict(fussballer_dto_mock)


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_success(fussballer_service: FussballerService, session_mock) -> None:
    # Arrange
    fussballer_id = 1
    username = "mocktest"
    email = "mock@email.test"
    nachname = "Mocktest"

    user_mock = User(
        username=username,
        email=email,
        nachname=nachname,
        vorname=nachname,
        roles=[Role.FUSSBALLER],
        password="p"
    )
    adresse_mock = Adresse(
        id=11,
        plz="12345",
        ort="Mockort",
        bundesland="Mockland",
        fussballer_id=fussballer_id,
        fussballer=None,
    )
    fussballer_mock = Fussballer(
        id=fussballer_id,
        nachname="Mocktest",
        nationalitaet="DE",
        position=Position.STUERMER,
        username=username,
        adresse=adresse_mock,
        auszeichnungen=[]
    )
    adresse_mock.fussballer: Fussballer = fussballer_mock
    fussballer_dto_mock = FussballerDTO(fussballer=fussballer_mock)
    session_mock.scalar.return_value = fussballer_mock

    # Act
    fussballer_dto: FussballerDTO = fussballer_service.find_by_id(
        fussballer_id=fussballer_id, user=user_mock
        )

    # Assert
    assert asdict(fussballer_dto) == asdict(fussballer_dto_mock)


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_not_found(fussballer_service: FussballerService, session_mock) -> None:
    # Arrange
    fussballer_id = 999
    user_mock = User(
        username="mocktest",
        email="mock@test.de",
        nachname="Mocktest",
        vorname="Mocktest",
        roles=[Role.ADMIN],
        password="p"
    )
    session_mock.scalar.return_value = None

    # Act
    with raises(NotFoundError) as err:
        fussballer_service.find_by_id(fussballer_id=fussballer_id, user=user_mock)

    # Assert
    assert err.type == NotFoundError
    assert str(err.value) == "Not Found"
    assert err.value.fussballer_id == fussballer_id


@mark.unit
@mark.unit_find_by_id
def test_find_by_id_not_found_admin(
    fussballer_service: FussballerService, session_mock
    ) -> None:
    # Arrange
    fussballer_id = 999
    user_mock = User(
        username="mocktest",
        email="mock@test.de",
        nachname="Mocktest",
        vorname="Mocktest",
        roles=[],
        password="p"
    )
    session_mock.scalar.return_value = None

    # Act
    with raises(ForbiddenError) as err:
        fussballer_service.find_by_id(fussballer_id=fussballer_id, user=user_mock)

    # Assert
    assert err.type == ForbiddenError
