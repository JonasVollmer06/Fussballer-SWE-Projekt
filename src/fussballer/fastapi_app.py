"""MainApp."""

from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from time import time
from typing import Any, Final

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from fussballer.banner import banner
from fussballer.config import dev_db_populate, dev_keycloak_populate
from fussballer.config.dev.db_populate import db_populate
from fussballer.config.dev.db_populate_router import router as db_populate_router
from fussballer.config.dev.keycloak_populate import keycloak_populate
from fussballer.config.dev.keycloak_populate_router import (
    router as keycloak_populate_router,
)
from fussballer.graphql_api import graphql_router
from fussballer.problem_details import create_problem_details
from fussballer.repository.session_factory import engine
from fussballer.router import (
    fussballer_router,
    fussballer_write_router,
    health_router,
    shutdown_router,
)
from fussballer.security import AuthorizationError, LoginError, set_response_headers
from fussballer.security import router as auth_router
from fussballer.service import (
    ForbiddenError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)

__all__ = [
    "authorization_error_handler",
    "login_error_handler",
    "not_found_error_handler",
    "version_outdated_error_handler",
]

TEXT_PLAIN: Final = "text/plain"


# --------------------------------------------------------------------------------------
# S t a r t u p   u n d   S h u t d o w n
# --------------------------------------------------------------------------------------
# https://fastapi.tiangolo.com/advanced/events
# pylint: disable=redefined-outer-name
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: RUF029
    """DB und Keycloak neu laden, falls im dev-Modus, sowie Banner in der Konsole."""
    if dev_db_populate:
        db_populate()
    if dev_keycloak_populate:
        keycloak_populate()
    banner(app.routes)
    yield
    logger.info("Der Server wird heruntergefahren")
    logger.info("Connection-Pool fuer die DB wird getrennt.")
    engine.dispose()


app: Final = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

app.add_middleware(GZipMiddleware, minimum_size=500)  # ty:ignore[invalid-argument-type]


@app.middleware("http")
async def log_request_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    logger.debug(f"{request.method} '{request.url}'")
    return await call_next(request)


@app.middleware("http")
async def log_response_time(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time()
    response = await call_next(request)
    duration_ms = (time() - start) * 1000
    logger.debug(
        f"Response time: {duration_ms:.2f} ms, statuscode: {response.status_code}"
    )
    return response


# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(fussballer_router, prefix="/rest")
app.include_router(fussballer_write_router, prefix="/rest")
app.include_router(auth_router, prefix="/auth")
app.include_router(health_router, prefix="/health")
app.include_router(shutdown_router, prefix="/admin")

if dev_db_populate:
    app.include_router(db_populate_router, prefix="/dev")
if dev_keycloak_populate:
    app.include_router(keycloak_populate_router, prefix="/dev")


# --------------------------------------------------------------------------------------
# G r a p h Q L
# --------------------------------------------------------------------------------------
app.include_router(graphql_router, prefix="/graphql")


# --------------------------------------------------------------------------------------
# S e c u r i t y
# --------------------------------------------------------------------------------------
# https://fastapi.tiangolo.com/tutorial/middleware
@app.middleware("http")
async def add_security_headers(
    request: Request,
    call_next: Callable[[Any], Awaitable[Response]],
) -> Response:
    """Header-Daten beim Response für IT-Sicherheit setzen.

    :param request: Injiziertes Request-Objekt, das zunächst fertig verarbeitet wird
    :param call_next: nächste aufzurufende Middleware
    :return: Response-Objekt mit zusätzlichen Header-Daten
    :rtype: Response
    """
    response: Final[Response] = await call_next(request)
    set_response_headers(response)
    return response


# --------------------------------------------------------------------------------------
# E x c e p t i o n   H a n d l e r
# --------------------------------------------------------------------------------------
@app.exception_handler(NotFoundError)
def not_found_error_handler(_request: Request, _err: NotFoundError) -> Response:
    """Errorhandler für NotFoundError.

    :param _err: NotFoundError aus der Geschäftslogik
    :return: Response mit Statuscode 404
    :rtype: Response
    """
    return create_problem_details(status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(ForbiddenError)
def forbidden_error_handler(_request: Request, _err: ForbiddenError) -> Response:
    """Errorhandler für ForbiddenError.

    :param _err: ForbiddenError vom Überprüfen der erforderlichen Rollen
    :return: Response mit Statuscode 403
    :rtype: Response
    """
    return create_problem_details(status_code=status.HTTP_403_FORBIDDEN)


@app.exception_handler(AuthorizationError)
def authorization_error_handler(
    _request: Request,
    _err: AuthorizationError,
) -> Response:
    """Errorhandler für AuthorizationError.

    :param _err: AuthorizationError vom Extrahieren der Benutzerkennung aus dem
        Authorization-Header
    :return: Response mit Statuscode 401
    :rtype: Response
    """
    return create_problem_details(status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(LoginError)
# pylint: disable-next=invalid-name
def login_error_handler(_request: Request, err: LoginError) -> Response:
    """Exception-Handler, wenn der Benutzername oder das Passwort fehlerhaft ist.

    :param _exc: LoginError
    :return: Response-Objekt mit Statuscode 401
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err)
    )


@app.exception_handler(UsernameExistsError)
def username_exists_error_handler(
    _request: Request,
    err: UsernameExistsError,
) -> Response:
    """Exception-Handling für UsernameExistsError.

    :param err: Exception, falls der Username für den neuen Patienten bereits existiert
    :return: Response mit Statuscode 422
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(err),
    )


@app.exception_handler(VersionOutdatedError)
def version_outdated_error_handler(
    _request: Request,
    err: VersionOutdatedError,
) -> Response:
    """Exception-Handling für VersionOutdatedError.

    :param _err: Exception, falls die Versionsnummer zum Aktualisieren veraltet ist
    :return: Response mit Statuscode 412
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail=str(err),
    )
