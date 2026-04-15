"""FussballWriteRouter."""
from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from fussballer.problem_details import create_problem_details
from fussballer.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from fussballer.router.dependencies import get_write_service
from fussballer.router.fussballer_model import FussballerModel
from fussballer.router.fussballer_update_model import FussballerUpdateModel
from fussballer.security import Role, RolesRequired
from fussballer.service import FussballerWriteService

__all__ = ["fussballer_write_router"]

fussballer_write_router: Final = APIRouter(tags=["Schreiben"])


@fussballer_write_router.post("")
def post(
    fussballer_model: FussballerModel,
    request: Request,
    service: Annotated[FussballerWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um einen neuen Fussballer anzulegen.

    :param fussballer_model: Fussballerdaten als Pydantic-Model
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit der Request-URL
    :param service: Injizierter Service für Geschäftslogik
    :rtype: Response
    :raises ValidationError: Falls es bei Pydantic Validierungsfehler gibt
    :raises UsernameExistsError: Falls der Benutzername bereits existiert
    """
    logger.debug("fussballer_model={}", fussballer_model)
    fussballer_dto: Final = service.create(fussballer=fussballer_model.to_fussballer())
    logger.debug("fussballer_dto={}", fussballer_dto)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{fussballer_dto.id}"},
    )


@fussballer_write_router.put(
    "/{fussballer_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.FUSSBALLER]))],
)
def put(
    fussballer_id: int,
    fussballer_update_model: FussballerUpdateModel,
    request: Request,
    service: Annotated[FussballerWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um einen Fussballer zu aktualisieren.

    :param fussballer_id: ID des zu aktualisierenden Fussballers als Pfadparameter
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit If-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    :raises ValidationError: Falls es bei Marshmallow Validierungsfehler gibt
    :raises NotFoundError: Falls zur id kein Fussballer existiert
    :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
    """
    if_match_value: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "fussballer_id={}, if_match={}, fussballer_update_model={}",
        fussballer_id,
        if_match_value,
        fussballer_update_model,
    )

    if if_match_value is None:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        )

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    fussballer: Final = fussballer_update_model.to_fussballer()
    fussballer_modified: Final = service.update(
        fussballer=fussballer,
        fussballer_id=fussballer_id,
        version=version_int,
    )
    logger.debug("fussballer_modified={}", fussballer_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETAG": f'"{fussballer_modified.version}'},
    )


@fussballer_write_router.delete(
    "/{fussballer_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.FUSSBALLER]))],
)
def delete_by_id(
    fussballer_id: int,
    service: Annotated[FussballerWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um einen Fussballer anhand seiner ID zu löschen.

    :param fussballer_id: ID des zu löschenden Fussballers
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    """
    logger.debug("fussballer_id={}", fussballer_id)
    service.delete_by_id(fussballer_id=fussballer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
