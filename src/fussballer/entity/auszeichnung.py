"""Entity-Klasse für Auszeichnung."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fussballer.entity.base import Base


class Auszeichnung(Base):
    """Entity-Klasse für Auszeichnung."""

    __tablename__ = "auszeichnung"

    bezeichnung: Mapped[str]
    """Name der Auszeichnung."""

    saison: Mapped[str]
    """Saison in der der Fußballspieler die Auszeichnung erhalten hat [20xx/yy]."""

    id: Mapped[int] = mapped_column(
        Identity(start=100),
        primary_key=True,
    )
    """Die generierte ID."""

    fussballer_id: Mapped[int] = mapped_column(ForeignKey("fussballer.id"))
    """ID des zugehörigen Fußballers als Fremdschlüssel in der Datenbank."""

    fussballer: Mapped[Fussballer] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable ]
        back_populates="auszeichnungen",
    )
    """Das Fußballer-Objekt."""
