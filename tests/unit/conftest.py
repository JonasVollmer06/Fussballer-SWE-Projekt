"""Fixtures für das Mocking von Repositories und Secuirty-Services."""

from keycloak import KeycloakAdmin
from pytest import fixture
from pytest_mock import MockerFixture

from fussballer.repository import FussballerRepository
from fussballer.security import UserService
from fussballer.service import FussballerService, FussballerWriteService


@fixture()
def fussballer_repository() -> FussballerRepository:
    """Stellt ein isoliertes FussballerRepository für Tests bereit."""
    return FussballerRepository()


@fixture
def fussballer_service(
    fussballer_repository: FussballerRepository,
) -> FussballerService:
    """Stellt den Lese_Service mit gemocktem Repository bereit."""
    return FussballerService(fussballer_repository)


@fixture
def keycloak_admin_mock(mocker: MockerFixture) -> KeycloakAdmin:
    """Mockt die KeycloakAdmin-Klasse, um echte Netzwerkanfragen zu verhindern."""
    keycloak_admin_cls_mock = mocker.patch(
        "fussballer.security.user_service.KeycloakAdmin"
    )
    return keycloak_admin_cls_mock.return_value


@fixture
def user_service(keycloak_admin_mock) -> UserService:
    """Stellt einen UserService mit simulierten Keycloak-Rollen bereit."""
    uuid_mock = "12345678-1234-1234-123456789012"
    keycloak_admin_mock.get_client_id.return_value = uuid_mock

    fussballer_rolle_mock = {
        "id": uuid_mock,
        "name": "fussballer",
        "description": "Basis-Rolle für Fussballer",
        "composite": False,
        "clientRole": True,
        "containerId": uuid_mock,
    }
    keycloak_admin_mock.get_client_roles.return_value = [fussballer_rolle_mock]
    return UserService()


@fixture
def fussballer_write_service(
    fussballer_repository: FussballerRepository, user_service: UserService
) -> FussballerWriteService:
    """Stellt den Schreib-Service mit allen benötigten Mocks bereit."""
    return FussballerWriteService(fussballer_repository, user_service)
