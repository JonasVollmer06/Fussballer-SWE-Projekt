"""Pydantic-Model zum Aktualisieren von Fussballer-Daten."""
from datetime import date
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

from fussballer.entity.fussballer import Fussballer
from fussballer.entity.position import Position
from fussballer.router.adresse_model import AdresseModel

__all__: list[str] = ["FussballerUpdateModel"]


class FussballerUpdateModel(BaseModel):
    """Pydantic-Model für das Aktualisiere von Fussballer-Daten."""

    nachname: Annotated[
        str,
        StringConstraints(
            pattern="^[A-ZÄÖÜ][A-Za-zÄÖÜäöüß-]*$",
            max_length=64,
        ),
    ]
    """Der Nachname."""
    position: Position | None = None
    """Die Position."""
    geburtsdatum: date
    """Das Geburtsdatum."""
    nationalitaet: Annotated[
        str,
        StringConstraints(
            pattern="^[A-ZÄÖÜ][A-Za-zÄÖÜäöüß-]*$",
            max_length=64,
        ),
    ]
    """Die Nationalitaet."""
    username: Annotated[str | None, StringConstraints(max_length=20)] = None
    """Optionaler Benutzername für ein Update."""
    adresse: AdresseModel | None = None
    """Optionale Adresse für Validierung bei Updates."""

    @field_validator("position", mode="before")
    @classmethod
    def _map_position(cls, value: str | Position | None) -> str | Position | None:
        if not isinstance(value, str):
            return value

        position_mapping = {
            "TORWART": Position.TORWART,
            "VERTEIDIGER": Position.VERTEIDIGER,
            "MITTELFELDSPIELER": Position.MITTELFELDSPIELER,
            "STUERMER": Position.STUERMER,
        }
        return position_mapping.get(value, value)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nachname": "Test",
                "position": "TW",
                "geburtsdatum": "2020-01-01",
                "nationalitaet": "Deutsch",
            },
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Konvertierung der primitiven Attribute in ein Dictionary.

        :return: Dictionary mit den primitiven Fussballer-Attributen
        :rtype: dict[str, Any]
        """
        fussballer_dict = self.model_dump()
        fussballer_dict["id"] = None
        fussballer_dict["adresse"] = None
        fussballer_dict["auszeichnungen"] = []
        fussballer_dict["erzeugt"] = None
        fussballer_dict["aktualisiert"] = None

        return fussballer_dict

    def to_fussballer(self) -> Fussballer:
        """Konvertierung in ein Fussballer-Objekt für SQLAlchemy.

        :return: Fussballer-Objekt für SQLAlchemy
        :rtype: Fussballer
        """
        fussballer_dict: dict[str, Any] = self.to_dict()

        return Fussballer(**fussballer_dict)
