"""FußballerGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from fussballer.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from fussballer.router.dependencies import get_service
from fussballer.security import Role, RolesRequired, User
from fussballer.service import FussballerDTO, FussballerService

__all__: list[str] = ["fussballer_router"]

fussballer_router: Final = APIRouter(tags=["Lesen"])


@fussballer_router.get(
    "/{fussballer_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.PATIENT]))],
)
def get_by_id(
    fussballer_id: int,
    request: Request,
    service: Annotated[FussballerService, Depends(get_service)],
) -> Response:
    """Suche mit der Fussballer-ID.

    :param fussballer_id: ID des gesuchten Fußballers als Pfadparameter
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit ggf. If-None-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit dem gefundenen Fußballerdatensatz
    :rtype: Response
    :raises NotFoundError: Falls kein Fußballer gefunden wurde
    :raises ForbiddenError: Falls die Fußballerdaten nicht gelesen werden dürfen
    """
    # User-Objekt ist durch Depends(RolesRequired()) in Request.state gepuffert
    user: Final[User] = request.state.current_user
    logger.debug("fussballer_id={}, user={}", fussballer_id, user)

    fussballer: Final = service.find_by_id(fussballer_id=fussballer_id, user=user)
    logger.debug("{}", fussballer)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version: str = if_none_match[1:-1]
        logger.debug("version={}", version)
        if version is not None:
            try:
                if int(version) == fussballer.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                logger.debug("invalid version={}", version)

    return JSONResponse(
        content=_fussballer_to_dict(fussballer),
        headers={ETAG: f'"{fussballer.version}"'},
    )


def _fussballer_to_dict(fussballer: FussballerDTO) -> dict[str, Any]:
    fussballer_dict: Final = asdict(obj=fussballer)
    fussballer_dict.pop("version")
    fussballer_dict.update({"geburtsdatum": fussballer.geburtsdatum.isoformat()})
    return fussballer_dict
