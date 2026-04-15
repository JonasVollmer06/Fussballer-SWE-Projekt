"""Modul für den Zugriff auf Service Methoden."""

from fussballer.service.adresse_dto import AdresseDTO
from fussballer.service.exceptions import (
    ForbiddenError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)
from fussballer.service.fussballer_dto import FussballerDTO
from fussballer.service.fussballer_service import FussballerService
from fussballer.service.fussballer_write_service import FussballerWriteService
from fussballer.service.mailer import send_mail

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "AdresseDTO",
    "ForbiddenError",
    "FussballerDTO",
    "FussballerService",
    "FussballerWriteService",
    "NotFoundError",
    "UsernameExistsError",
    "VersionOutdatedError",
    "send_mail",
]
