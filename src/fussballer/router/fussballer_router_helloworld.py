"""Fußballer Router fpr eine Hello World Get-Request."""

from typing import Final

from fastapi import APIRouter

__all__: list[str] = ["fussballer_router_hello_world"]

fussballer_router_hello_world: Final = APIRouter(tags=["Lesen"])


@fussballer_router_hello_world.get(path="/testpath")
def test() -> dict[str, str]:
    """Ein Router zum Testen."""
    return {"msg": "Hello World!"}
