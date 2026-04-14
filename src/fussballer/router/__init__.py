"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from fussballer.router.fussballer_model import FussballerModel
from fussballer.router.fussballer_router import (
    fussballer_router,
    get,
    get_by_id,
    get_nachname,
)
from fussballer.router.fussballer_router_helloworld import (
    fussballer_router_hello_world,
    test,
)
from fussballer.router.fussballer_write_router import (
    delete_by_id,
    fussballer_write_router,
    post,
    put,
)
from fussballer.router.health_router import liveness, readiness
from fussballer.router.health_router import router as health_router
from fussballer.router.shutdown_router import router as shutdown_router
from fussballer.router.shutdown_router import shutdown

__all__: Sequence[str] = [
    "FussballerModel",
    "delete_by_id",
    "fussballer_router",
    "fussballer_router_hello_world",
    "fussballer_write_router",
    "get",
    "get_by_id",
    "get_nachname",
    "health_router",
    "liveness",
    "post",
    "put",
    "readiness",
    "shutdown",
    "shutdown_router",
    "test",
]
