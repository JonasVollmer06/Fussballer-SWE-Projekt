"""Router zur Statusabfrage des Servers."""

from typing import Any, Final

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from fussballer.repository import engine

__all__ = ["router"]

router: Final = APIRouter(tags=["Health"])


@router.get("/liveness")
def liveness() -> dict[str, Any]:
    """Methode zum liefern einer Statusmeldung über Liveness-Status."""
    return {"status": "up"}


@router.get("readisness")
def readiness() -> dict[str, Any]:
    """Methode zum liefern einer Statusmeldung über Readiness-Status."""
    with engine.connect() as connection:
        try:
            connection.scalar(text("SELECT 1"))
        except OperationalError:
            return {"db": "down"}

    return {"db": "up"}
