"""Modul für den Zugriff auf Service Methoden."""

from fussballer.service.adresse_dto import AdresseDTO
from fussballer.service.exceptions import ForbiddenError, NotFoundError
from fussballer.service.fussballer_dto import FussballerDTO
from fussballer.service.fussballer_service import FussballerService

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "AdresseDTO",
    "ForbiddenError",
    "FussballerDTO",
    "FussballerService",
    "NotFoundError",
]
