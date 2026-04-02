"""Geschäftslogik zum Lesen von Fussballer-Daten."""

from collections.abc import Mapping, Sequence
from typing import Final

from fussballer.repository import (
    FussballerRepository,
    Pageable,
    Session,
    Slice,
)
from fussballer.security import Role, User
from fussballer.service import FussballerDTO
from fussballer.service.exceptions import ForbiddenError, NotFoundError

__all__ = ["FussballerService"]


class FussballerService:
    """Service-Klasse mit Geschäftslogik für Fussballer."""

    def __init__(self, repo: FussballerRepository) -> None:
        """Konstruktor mit Repository für Fussballer-Objekte."""
        self.repo: FussballerRepository = repo

    def find_by_id(self,
    fussballer_id: int,
    user: User) -> FussballerDTO:
        """Suche von Fussballern anhand übergebener ID.

        :return: Gefundenes FussballerDTO Objekt zu passender ID.
        """
        with Session() as session:
            user_is_admin: Final = Role.ADMIN in user.roles

            if (
                fussballer := self.repo.find_by_id(fussballer_id, session)
            ) is None:
                raise NotFoundError(fussballer_id=fussballer_id)
                """Es konnte kein Fussballer-Objekt zur gegeben ID gefunden werden."""
            if user_is_admin:
                raise ForbiddenError

            if fussballer.username != user.username and not user_is_admin:
                raise ForbiddenError

            fussballer_dto: Final = FussballerDTO(fussballer)
            session.commit()
        return fussballer_dto

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable
    ) -> Slice[FussballerDTO]:
        """Suche von Fussballern anhand Query-Parametern.

        :return: Fussballer-Objekte Liste zu den Query-Parametern.
        """
        with Session() as session:
            fussballer_slice: Final = self.repo.find(suchparameter, pageable, session)
            if len(fussballer_slice.content) == 0:
                raise NotFoundError(suchparameter=suchparameter)

            fussballers_dto: Final = tuple(
                FussballerDTO(fussballer) for fussballer in fussballer_slice.content
            )
            session.commit()

        return Slice(content=fussballers_dto,
            total_elements=fussballer_slice.total_elements)

    def find_nachnamen(self, teil: str) -> Sequence[str]:
        """Suche einen passenden Fussballer Nachname zu einem gegebenen Teilstring.

        :return: Eine Sqeuenz mit den gefundenen Nachnamen, da eine Sequenz allgemeiner
        als eine Liste ist und man sich somit nicht unnötiger weiße konkret auf eine
        Liste.
        """
        with Session() as session:
            nachnamen: Final = self.repo.find_nachnamen(teil, session)
            session.commit()

            if len(nachnamen) == 0:
                raise FileNotFoundError

            return nachnamen
