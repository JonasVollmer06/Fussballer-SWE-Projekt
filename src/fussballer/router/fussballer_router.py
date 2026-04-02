"""FußballerGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse

from fussballer.repository import Pageable
from fussballer.repository.slice import Slice
from fussballer.router.constants import IF_NONE_MATCH_MIN_LEN, PAGE, SIZE
from fussballer.router.dependencies import get_service
from fussballer.router.page import Page
from fussballer.security import Role, RolesRequired, User

__all__: list[str] = ["fussballer_router"]

fussballer_router: Final = APIRouter(tags=["Lesen"])


@fussballer_router.get(
    "/{fussballer_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.FUSSBALLER]))],
)
def get_by_id(
    fussballer_id: int,
    request: Request,
    service: Annotated[FussballerService, Depends(get_service)],
)   -> Response:
    """Suche eines Fußballer-Objektes durch eine vorgegebene ID.

    :param fussballer_id: Die ID zu welcher das passende Fußballer-Objekt gesucht wird
    :return: Response mit den Daten des gefundenen Objektes
    """
    user: Final[User] = request.state.current_user

    fussballer: Final = service.find_by_id(user, fussballer_id)

    if_none_match: Final = request.headers.get("if-none-match")

    if (
        if_none_match is not None and
        len(if_none_match) >= IF_NONE_MATCH_MIN_LEN and
        if_none_match.startswith('"') and
        if_none_match.endswith('"')
    ):
        versionsnummer = if_none_match[1:-1]
        if versionsnummer is not None:
            try:
                if int(versionsnummer) == fussballer.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                pass

    return JSONResponse(
        content=_fussballer_to_dict(fussballer),
        headers={"ETag": f'"{fussballer.version}"'},
    )


@fussballer_router.get(
     "/{fussballer_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.FUSSBALLER]))],
)
def get(
    request: Request,
    service: Annotated[FussballerService, Depends(get_service)],
) -> JSONResponse:
    """Suche von Fussballer-Objekten mit Query-Parametern.

    :return: Response mit einer Seite mit gefundenen Fussballer-Objekten zu den
    gegebenen Query-Parametern
    """
    query_parameter: Final = request.query_params

    page: Final = query_parameter.get(PAGE)
    size: Final = query_parameter.get(SIZE)
    pageable: Final = Pageable.create(page, size)

    suchparameter = dict(query_parameter)
    suchparameter.pop(PAGE, None)
    suchparameter.pop(SIZE, None)

    fussballer_slice: Final = service.find(suchparameter, pageable)

    result: Final = _fussballer_slice_to_page(fussballer_slice, pageable)
    return JSONResponse(content=result)


@fussballer_router.get(
    "/nachname/{teil}",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get_by_nachname(
    teil: str,
    service: Annotated[FussballerService, Depends(get_service)],
) -> JSONResponse:
    """Suche von Fussballer-Nachnamen anhand von übergebenen Teilstrings.

    :param teil: Übergebener Teilstring, zum Suchen von Fussballer-Nachnamen
    :return: Rückgabe ist der gefundene Nachname passend zum Teilstring
    """
    nachnamen: Final = service.find_nachnamen(teil)
    return JSONResponse(content=nachnamen)


def _fussballer_slice_to_page(
    fussballer_slice: Slice[FussballerDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    fussballer_dict: Final = tuple(
        _fussballer_to_dict(fussballer) for fussballer in fussballer_slice.content
    )
    page: Final = Page.create(
        content=fussballer_dict,
        pageable=pageable,
        total_elements=fussballer_slice.total_elements,
    )
    return asdict(obj=page)


def _fussballer_to_dict(fussballer: FussballerDTO) -> dict[str, Any]:
    fussballer_dict: Final = asdict(obj=fussballer)
    fussballer_dict.pop("version")
    fussballer_dict.update({"geburtsdatum": fussballer.geburtsdatum.isoformat()})
    """Geburtsdatum wird von einem Date-Format in einen standardisierten String
    umgewandelt.
    """
    return fussballer_dict
