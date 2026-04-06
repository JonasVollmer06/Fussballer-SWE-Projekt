"""FussballWriteRouter."""
from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status

from fussballer.problem_details import create_problem_details
from fussballer.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from fussballer.router.dependencies import get_write_service
from fussballer.router.fussballer_model import FussballerModel
from fussballer.router.fussballer_update_model import FussballerUpdateModel
from fussballer.security import Role, RolesRequired
from fussballer.service import FussballerWriteService

__all__ = ["fussballer_write_router"]

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
    :raises EmailExistsError: Falls die Emailadresse bereits existiert
    :raises UsernameExistsError: Falls der Benutzername bereits existiert
    """
    fussballer_dto: Final = service.create(fussballer=fussballer_model.to_fussballer())

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{fussballer_dto.id}"},
    )


@fussballer_write_router.put(
    "/{fussballer_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.FUSSBALLER]))],
)
def put(
    
)
