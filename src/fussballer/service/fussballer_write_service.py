"""Geschäftslogik für das Schreiben von Fussballer-Daten."""

from typing import Final

from fussballer.entity import Fussballer
from fussballer.repository import fussballerRepository, Session
from fussballer.security import User, UserService
from fussballer.service.exceptions import (
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)
from fussballer.service.mailer import send_mail
from fussballer.service.fussballer_dto import fussballerDTO

__all__: list[str] = ["FussballerWriteService"]


class FussballerWriteService:
    """Service-Klasse für Fussballer mit Geschäftslogik."""

    def __init__(self, repo: fussballerRepository, user_service: UserService) -> None:
        """Konstruktor mit FussballerRepository und UserService."""
        self.repo: FussballerRepository = repo
        self.user_service: UserService = user_service

    def create(self, fussballer: Fussballer) -> FussballerDTO:
        """Neuen Fussballer anlegen.

        :param fussballer: Der neue Fussballer ohne ID
        :return: Der neu angelegte Fussballer mit generierter ID
        :rtype: FussballerDTO
        """
        
