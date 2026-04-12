"""Unit-Tests für create() von FussbapperWriteService."""

from copy import deepcopy

from pytest import fixture, mark, raises
from pytest_mock import MockerFixture


from fussballer.entity import Adresse, Fussballer, Position
from fussballer.service import EmailExistsError, UsernameExistsError


@fixture
def session_mock(mocker: MockerFixture):
    session = mocker.Mock()
    mocker.patch(
        "fussballer.service.fussballer_write_service.Session",
        return_value=mocker.MagicMock(
            __enter__=lambda self: session,
            __exit__=lambda self, ecx_type, exc, tb: None,
        ),
    )
    return session


@mark.unit
@mark.unit_ceate
def test_create(
    fussballer_write_service, session_mock, keycloak_admin_mock, mocker
) -> None:
    # Arrange
    email = "mock@email.test"
    adresse = Adresse(
        id=999,
        plz="12345",
        ort="Mockort",
        bundesland="Mockland",
        fussballer_id=None,
        fussballer=None,
    )
    fussballer = Fussballer(
        id=None,
        email=email,
        nachname="Mocktest",
        nationalitaet="DE",
        position=Position.STUERMER,
        username="mocktest",
        adresse=adresse,
        auszeichnungen=[],
    )
    adresse.fussballer = fussballer
    fussballer_db_mock = deepcopy(fussballer)
    generierte_id = 1
    fussballer_db_mock.id = generierte_id
    fussballer_db_mock.adresse.id = generierte_id

    keycloak_admin_mock.get_user_id.return_value = None
    keycloak_admin_mock.get_users.return_value = []

    session_mock.scalar.return_value = 0
    session_mock.add.return_value = None

    def flush_side_effect(objects=None):
        for obj in objects or []:
            obj.id = generierte_id

    session_mock.flush.side_effect = flush_side_effect

    mocker.patch("fussballer.service.fussballer_write_service.send_mail", return_value=None)

    # Act
    fussballer_dto = fussballer_write_service.create(fussballer=fussballer)

    # Assert
    assert fussballer_dto.id == generierte_id
