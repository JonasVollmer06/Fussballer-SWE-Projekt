"""Entity-Klasse für Fußballerdaten."""

from datetime import date, datetime
from typing import Any, Self

from sqlalchemy import Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fussballer.entity.adresse import Adresse
from fussballer.entity.auszeichnung import Auszeichnung
from fussballer.entity.base import Base
from fussballer.entity.position import Position


class Fussballer(Base):tt
    """Entity-Klasse für Fußballerdaten."""

    __tablename__ = "fussballer"

    nachname: Mapped[str]
    """Der Nachname des Fussballers."""

    position: Mapped[Position | None]
    """Die optionale Position des Fußballspielers."""

    geburtsdatum: Mapped[date]
    """Das Geburtsdatum des Fußballspielers."""

    nationalitaet: Mapped[str]
    """Herkunft des Fußballspielers(Geburtsort)."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=100),
        primary_key=True,
    )

    adresse: Mapped[Adresse] = relationship(
        back_populates="fussballer",
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Die in einer 1:1-Beziehung referenzierte Adresse."""

    auszeichnungen: Mapped[list[Auszeichnung]] = relationship(
        back_populates="fussballer",
        cascade="save-update, delete",
    )

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Die Versionsnummer für Lost Updates."""

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
    """Der Zeitstempel für die Datenbank."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )
    """Der Zeitstempel für Änderungen in der Datenbank"""

    __mapper_args__ = {"version_id_col": version}

    def set(self, fussballer: Self) -> None:
        """Primitive Attributwerte überschreiben, z.B. vor DB-Update."""
        self.nachname: str = fussballer.nachname
        self.nationalitaet: str = fussballer.nationalitaet
        self.geburtsdatum: date = fussballer.geburtsdatum

    def __eq__(self, other: Any) -> bool:
        """Vergleich auf Gleichheit, ohne Joins zu verursachen."""
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Funktion anhand der ID, ohne Joins zu verursachen."""
        return hash(self.id) if self.id is not None else hash(type(self))

    def __repr__(self) -> str:
        """Ausgabe eines Fussballers als String, ohne Joins zu verursachen."""
        return (
            f"Fussballer(id={self.id}, version={self.version}, "
            + f"nachname={self.nachname}, position={self.position}, "
            + f"geburtsdatum={self.geburtsdatum}, nationalitaet={self.nationalitaet}, "
            + f"erzeugt={self.erzeugt}, aktualisiert={self.aktualisiert})"
        )
