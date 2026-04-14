"""Router für den Shutdown in REST-API."""

import os
import signal
from typing import Any, Final

from fastapi import APIRouter, Depends

from fussballer.security.role import Role
from fussballer.security.roles_required import RolesRequired

__all__ = ["router"]

router: Final = APIRouter(tags=["Admin"])


@router.post("/shutdown", dependencies=[Depends(RolesRequired(Role.ADMIN))])
def shutdown() -> dict[str, Any]:
    """Methode zum Herunterfahren des Servers."""
    os.kill(os.getpid(), signal.SIGINT)  # NOSONAR
    return {"message": "Server is shutting down..."}
