"""Geschäftslogik für das Schreiben von Fussballer-Daten."""

from typing import Final

from fussballer.entity import Fussballer
from fussballer.repository import FussballerRepository, Session
from fussballer.security import User, UserService
from fussballer.service.exceptions import (
    EmailExistsError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)
from fussballer.service.fussballer_dto import FussballerDTO
from fussballer.service.mailer import send_mail

__all__: list[str] = ["FussballerWriteService"]


class FussballerWriteService:
    """Service-Klasse für Fussballer mit Geschäftslogik."""

    def __init__(self, repo: FussballerRepository, user_service: UserService) -> None:
        """Konstruktor mit FussballerRepository und UserService."""
        self.repo: FussballerRepository = repo
        self.user_service: UserService = user_service

    def create(self, fussballer: Fussballer) -> FussballerDTO:
        """Neuen Fussballer anlegen.

        :param fussballer: Der neue Fussballer ohne ID
        :return: Der neu angelegte Fussballer mit generierter ID
        :rtype: FussballerDTO
        """
        username: Final = fussballer.username
        if username is None:
            raise ValueError("Username darf nicht None sein.")

        if self.user_service.username_exists(username):
            raise UsernameExistsError(username)

        user: Final = User(
            username=username,
            email=f"{username}@acme.com",
            vorname=fussballer.nachname,
            nachname=fussballer.nachname,
            password="p",  # noqa: S106 # NOSONAR
            roles=[],
        )
        self.user_service.create_user(user)

        with Session() as session:

            fussballer_db: Final = self.repo.create(
                fussballer=fussballer, session=session
                )
            fussballer_dto: Final = FussballerDTO(fussballer_db)
            session.commit()

            send_mail(fussballer_dto=fussballer_dto)
            return fussballer_dto

    def update(
        self, fussballer: Fussballer, fussballer_id: int, version: int
        ) -> FussballerDTO:
        """Daten eines Fussballers ändern.

        :param fussballer: Die neuen Daten
        :param fussballer_id: ID des zu aktualisierenden Fussballers
        :param version: Version für optimistische Synchronisation
        :return: Der aktualisierte Fussballer
        :rtype: FussballerDTO
        :raises NotFoundError: Fussballer existiert nicht
        :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        """
        with Session() as session:
            if (
                fussballer_db := self.repo.find_by_id(
                    fussballer_id=fussballer_id, session=session
                )
            ) is None:
                raise NotFoundError(fussballer_id=fussballer_id)
            if fussballer_db.version > version:
                raise VersionOutdatedError(version)

            fussballer_db.set(fussballer)
            if (
                fussballer_updated := self.repo.update(fussballer=fussballer_db,
                session=session)
            ) is None:
                raise NotFoundError(fussballer_id=fussballer_id)
            fussballer_dto: Final = FussballerDTO(fussballer_updated)

            session.commit()
            fussballer_dto.version += 1
            return fussballer_dto

    def delete_by_id(self, fussballer_id: int) -> None:
        """Einen Fussballer anhand seiner ID löschen.

        :param fussballer_id: ID des zu löschenden Fussballers
        """
        with Session() as session:
            self.repo.delete_by_id(fussballer_id, session=session)
            session.commit()
