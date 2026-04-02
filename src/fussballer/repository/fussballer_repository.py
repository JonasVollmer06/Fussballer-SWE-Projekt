"""Repository für Fußballer-Microservice."""

from collections.abc import Mapping, Sequence
from typing import Final

from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from fussballer.entity import Fussballer
from fussballer.repository.pageable import Pageable
from fussballer.repository.slice import Slice


__all__ = ["FussballerRepository"]


class FussballerRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Fußballer."""

    def find_by_id(self, fussballer_id, session) -> Fussballer | None:
        """Datenbankzugriff für das Suchen von Fussballer-Objekt mit einer ID."""
        if fussballer_id is None:
            return None

        statement: Final = (
            select(Fussballer)
            .options(joinedload(Fussballer.adresse))
            .where(fussballer_id == Fussballer.id)
        )
        fussballer: Final = session.scalar(statement)

        return fussballer


    def find(self, suchparameter: Mapping[str, str], pageable: Pageable,
        session: Session) -> Slice[Fussballer]:
        """Suche von Fussballer-Objekten mit Suchparametern.

        :return: Ausschnitt der gefundenen Fussballer-Objekten
        """
        if not suchparameter:
            return self._find_all(pageable, session)
        """Rückgabe aller Fussballer-Objekte im Falle einer Leeren Liste, welche
        durch is None nicht erkannt werden würde."""

        for key, value in suchparameter.items():
            if key == "nachname":
                fussballers = self._find_by_nachname(
                    teil=value, pageable=pageable, session=session)


    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Fussballer]:
        """Fussballer-Objekte Ausschnittweise bei leerer Suchparameter-Liste."""
        start = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = (
                    select(Fussballer)
                    .options(joinedload(Fussballer.adresse))
                    .limit(pageable.size)
                    .offset(start)
            )
        else:
            statement: Final = (
                select(Fussballer)
                .options(joinedload(Fussballer.adresse))
            )

        fussballers: Final = (session.scalars(statement)).all()
        anzahl: Final = self._count_all_rows(session)
        fussballer_slice: Final = Slice(content=tuple(fussballers),
            total_elements=anzahl)

        return fussballer_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Fussballer)
        count: Final = session.execute(statement).scalar()

        return count if count is not None else 0

    def _find_by_nachname(self, teil: str, pageable: Pageable,
    session: Session) -> Slice[Fussballer]:

        start = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = (
                select(Fussballer)
                .options(joinedload(Fussballer.adresse))
                .filter(Fussballer.nachname.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(start)
            )
        else:
            statement: Final = (
                select(Fussballer)
                .options(joinedload(Fussballer.adresse))
                .filter(Fussballer.nachname.ilike(f"%{teil}%"))
            )
        """Flexible Suche nach Nachnamen mit einem Teilstring durch
        caseinsensitives ilike."""

        fussballers: Final = session.scalars(statement).all()
        anzahl: Final = self._count_nachname_rows(teil, session)
        fussballer_slice: Final = Slice(content=tuple(fussballers),
            total_elements=anzahl)

        return fussballer_slice

    def _count_nachname_rows(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Fussballer)
            .filter(Fussballer.nachname.ilike(f"%{teil}%"))
        )

        count: Final = session.execute(statement).scalar()

        if count is not None:
            return count
        return 0
        