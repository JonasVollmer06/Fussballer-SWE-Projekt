"""Repository für Fußballer-Microservice."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import InstrumentedAttribute, Session, joinedload

from fussballer.entity import Fussballer
from fussballer.repository.pageable import Pageable
from fussballer.repository.slice import Slice

__all__ = ["FussballerRepository"]


class FussballerRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Fußballer."""

    def find_by_id(self, fussballer_id, session) -> Fussballer | None:
        """Datenbankzugriff für das Suchen von Fussballer-Objekt mit einer ID."""
        logger.debug("fussballer_id: {}", fussballer_id)

        if fussballer_id is None:
            return None

        statement: Final = (
            select(Fussballer)
            .options(joinedload(Fussballer.adresse))
            .where(Fussballer.id == fussballer_id)
        )
        fussballer: Final = session.scalar(statement)
        logger.debug("Fussballer: {}", fussballer)

        return fussballer

    def find(
        self, suchparameter: Mapping[str, str], pageable: Pageable, session: Session
    ) -> Slice[Fussballer]:
        """Suche von Fussballer-Objekten mit Suchparametern.

        :return: Ausschnitt der gefundenen Fussballer-Objekten.
        """
        logger.debug("suchparameter: {}", suchparameter)
        if not suchparameter:
            return self._find_all(pageable, session)
        """Rückgabe aller Fussballer-Objekte im Falle einer Leeren Liste, welche
        durch is None nicht erkannt werden würde."""

        erlaubte_attribute = {
            "nachname": Fussballer.nachname,
            "nationalitaet": Fussballer.nationalitaet,
        }

        for key, value in suchparameter.items():
            if key not in erlaubte_attribute:
                raise ValueError

            attribut = erlaubte_attribute[key]

            return self._find_by_attribut(
                attribut, teil=value, pageable=pageable, session=session
            )

        logger.debug("slice: {}", Slice)
        return Slice(content=(), total_elements=0)

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
            statement: Final = select(Fussballer).options(
                joinedload(Fussballer.adresse)
            )

        fussballers: Final = (session.scalars(statement)).all()
        logger.debug("Fussballers: {}", fussballers)
        anzahl: Final = self._count_all_rows(session)
        fussballer_slice: Final = Slice(
            content=tuple(fussballers), total_elements=anzahl
        )

        return fussballer_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Fussballer)
        count: Final = session.execute(statement).scalar()

        return count if count is not None else 0

    def _find_by_attribut(
        self,
        attribut: InstrumentedAttribute,
        teil: str,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Fussballer]:

        start = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = (
                select(Fussballer)
                .options(joinedload(Fussballer.adresse))
                .filter(attribut.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(start)
            )
        else:
            statement: Final = (
                select(Fussballer)
                .options(joinedload(Fussballer.adresse))
                .filter(attribut.ilike(f"%{teil}%"))
            )
        """Flexible Suche nach Attribut mit einem Teilstring durch
        caseinsensitives ilike."""

        fussballers: Final = session.scalars(statement).all()
        anzahl: Final = self._count_attribut_rows(attribut, teil, session)
        fussballer_slice: Final = Slice(
            content=tuple(fussballers), total_elements=anzahl
        )

        return fussballer_slice

    def _count_attribut_rows(
        self, attribut: InstrumentedAttribute, teil: str, session: Session
    ) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Fussballer)
            .filter(attribut.ilike(f"%{teil}%"))
        )

        count: Final = session.execute(statement).scalar()

        if count is not None:
            return count
        return 0

    def find_nachnamen(self, teil: str, session: Session) -> Sequence[str]:
        """Nachnamen zu einem gegebenen Teilstring suchen."""
        statement: Final = (
            select(Fussballer.nachname)
            .filter(Fussballer.nachname.ilike(f"%{teil}%"))
            .distinct()
        )

        nachnamen: Final = (session.scalars(statement)).all()

        return nachnamen

    def create(self, fussballer: Fussballer, session: Session) -> Fussballer:
        """Erstellen eines neuen Fussballer-Objektes.

        :return: Das neu angelegte Fussballer-Objekt mit der neu generierten ID.
        """
        session.add(instance=fussballer)
        """Vormerken des Objektes in der Session."""
        session.flush(objects=[fussballer])
        """Ausführen des Inserts und generieren der ID."""

        return fussballer

    def update(self, fussballer: Fussballer, session: Session) -> Fussballer | None:
        """Ändern der Daten eines Fussballer-Objektes.

        :return: Das aktualisierte Fussballer-Objekt oder None wenn
        das Objekt nicht gefunden wurde.
        """
        if (fussballer_db := self.find_by_id(fussballer.id, session)) is None:
            return None

        return fussballer_db

    def delete_by_id(self, fussballer_id: int, session: Session) -> None:
        """Löschen von Fussballerdatensatz mit Adresse."""
        if (fussballer := self.find_by_id(fussballer_id, session)) is None:
            return
        session.delete(fussballer)
