"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from fussballer.repository.fussballer_repository import FussballerRepository
from fussballer.service.fussballer_service import FussballerService


def get_repository() -> FussballerRepository:
    """Factory-Funktion für FussballerRepository."""
    return FussballerRepository()


def get_service(
    repo: Annotated[FussballerRepository, Depends(get_repository)],
) -> FussballerService:
    """Factory-Funktion für FussballerService."""
    return FussballerService(repo=repo)
