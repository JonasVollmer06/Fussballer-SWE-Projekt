"""Pydantic-Model für die Adresse."""

from ty_extensions import Unknown

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from fussballer.entity import Adresse

__all__: list[str] = ["AdresseModel"]


class AdresseModel(BaseModel):
    """Pydantic-Model für die Adresse."""

    plz: Annotated[str, StringConstraints(pattern=r"^\d{5}$")]
    """Postleitzahl"""
    ort: Annotated[str, StringConstraints(max_length=64)]
    """Ort"""
    bundesland: Annotated[str, StringConstraints(max_length=21)]
    """Bundesland"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "plz": "12345",
                "ort": "Musterort",
                "bundesland": "Musterbundesland",
            },
        }
    )

    def to_adresse(self) -> Adresse:
        """Konvertierung in ein Adresse-Objekt für SQLAlchemy.

        :return: Adresse-Objekt für SQLAlchemy
        :rtype: Adresse
        """
        adresse_dict: Unknown = self.model_dump()
        adresse_dict["id"] = None
        adresse_dict["patient_id"] = None
        adresse_dict["patient"] = None

        return Adresse(**adresse_dict)
