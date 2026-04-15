"""REST-Schnittstelle für Login, um aus Anmeldedaten einen Token zu erstellen."""

from json import JSONDecodeError
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse

from fussballer.security.dependencies import get_token_service
from fussballer.security.login_data import LoginData
from fussballer.security.token_service import TokenService

__all__ = ["router"]

router: Final = APIRouter(tags=["Login"])

"""Liest den Https-Request-Body aus und versucht diesen inhalt aus JSON in ein
Dictionary zu parsen. Falls dies nicht möglich ist soll eine leere Liste zurückegegeben
werden.
"""


async def request_body_to_dict(request: Request) -> dict[str, Any]:
    try:
        body: dict[str, Any] = await request.json()
        return body
    except JSONDecodeError:
        return {}


@router.post("/token")
def token(
    body: Annotated[dict[str, Any], Depends(request_body_to_dict)],
    service: Annotated[TokenService, Depends(get_token_service)],
) -> Response:
    """Extrahierte Anmeldedaten verwenden um einen JWT-Token zu erhalten.

    Jedoch ist wie in request_body_to_dict zu sehen nicht garantiert,
    dass der Inhalt von body Daten enthält.
    """
    try:
        login_data: Final = LoginData(username=body["username"],
        password=body["password"])
    except (KeyError, TypeError):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    token: Final = service.token(username=login_data.username,
    password=login_data.password,
    )
    access_token: Final = token["access_token"]
    roles: Final = service.get_roles_from_token(token=access_token)

    response_body: Final = {
        "token": access_token,
        "expires_in": token["expires_in"],
        "rollen": roles,
    }
    return JSONResponse(content=response_body)
