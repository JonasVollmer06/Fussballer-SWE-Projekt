"""Pydantic-Model für die Auszeichnungen."""
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from fussballer.entity import Auszeichnung

__all__: list[str] = ["AuszeichnungModel"]


class AuszeichnungModel(BaseModel):
    """Pydantic-Model für die auszeichnung_dict."""

    bezeichnung: Annotated[
        str,
        StringConstraints(
            pattern="^[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß])?$",
            max_length=64,
        ),
    ]
    """Die Bezeichnung."""
    saison: Annotated[str, StringConstraints(pattern=r"^(\d{4})(\/\d{2})?$")]
    """Die Saison."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bezeichnung": "Bundesliga-Torschützenkönig",
                "saison": "2024/25",
            },
        }
    )

    def to_auszeichnung(self) -> Auszeichnung:
        """Konvertierung in ein Auszeichnung-Objekt für SQLAlchemy.

        :return: Auszeichnung-Objekt für SQLAlchemy
        :rtype: Auszeichnung
        """
        auszeichnung_dict = self.model_dump()
        auszeichnung_dict["id"] = None
        auszeichnung_dict["fussballer_id"] = None
        auszeichnung_dict["fussballer"] = None

        return Auszeichnung(**auszeichnung_dict)
