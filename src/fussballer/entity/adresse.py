"""Entity-Klasse für die Adresse."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from patient.entity.base import Base


class Adresse(Base):
    """Entity-Klasse für die Adresse."""

    __tablename__ = "adresse"

    plz: Mapped[str]
    """Die Postleitzahl des Fussballspielers."""

    ort: Mapped[str]
    """Der Wohnort des Spielers."""

    bundesland: Mapped[str]
    """Bundesland des Spielers."""

    id: Mapped[int] = mapped_column(
        Identity(start=100),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    fussballer_id: Mapped[int] = mapped_column(ForeignKey("fussballer.id"))
    """ID des zugehörigen Fußballspieler als Fremdschlüssel Datenbank."""

    fussballer: Mapped[Fussballer] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
        back_populates="adresse",
    )
    """Das zugehörige Fußballer-Objekt."""

    def __repr__(self) -> str:
        """ToString für Adresse-Objekte ohne Fußballer."""
        return (
            f"Adresse(id={self.id}, plz={self.plz}, ort={self.ort}, "
            + f"bundesland={self.bundesland})"
        )
