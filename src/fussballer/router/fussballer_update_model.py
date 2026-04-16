"""Pydantic-Model zum Aktualisieren von Fussballer-Daten."""
from datetime import date
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, StringConstraints

from fussballer.entity.fussballer import Fussballer
from fussballer.entity.position import Position

__all__: list[str] = ["FussballerUpdateModel"]


class FussballerUpdateModel(BaseModel):
    """Pydantic-Model für das Aktualisiere von Fussballer-Daten."""

    nachname: Annotated[
        str,
        StringConstraints(
            pattern="^[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß])?$",
           # pattern="^[A-ZÄÖÜ][A-Za-zÄÖÜäöüß-]*$",
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
            # pattern="^[A-ZÄÖÜ][A-Za-zÄÖÜäöüß-]*$",
            pattern="^[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß])?$",
            max_length=64,
        ),
    ]
    """Die Nationalitaet."""

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
        fussballer_dict["username"] = None
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
