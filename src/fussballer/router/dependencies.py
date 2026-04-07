"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from fussballer.repository.fussballer_repository import FussballerRepository
from fussballer.security.dependencies import get_user_service
from fussballer.security.user_service import UserService
from fussballer.service.fussballer_service import FussballerService
from fussballer.service.fussballer_write_service import FussballerWriteService



def get_repository() -> FussballerRepository:
    """Factory-Funktion für FussballerRepository."""
    return FussballerRepository()


def get_service(
    repo: Annotated[FussballerRepository, Depends(get_repository)],
) -> FussballerService:
    """Factory-Funktion für FussballerService."""
    return FussballerService(repo=repo)


def get_write_service(
    repo: Annotated[FussballerRepository, Depends(get_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> FussballerWriteService:
    """Factory-Funktion für FussballerWriteService."""
    return FussballerWriteService(repo=repo, user_service=user_service)
