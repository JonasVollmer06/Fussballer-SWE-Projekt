"""Pydantic-Model für die Fussballer-Daten."""

from typing import Annotated, Any, Final

from pydantic import StringConstraints

from fussballer.entity import Fussballer
from fussballer.entity.adresse import Adresse
from fussballer.entity.auszeichnung import Auszeichnung
from fussballer.router.adresse_model import AdresseModel
from fussballer.router.auszeichnung_model import AuszeichnungModel
from fussballer.router.fussballer_update_model import FussballerUpdateModel

__all__: list[str] = ["FussballerModel"]


class FussballerModel(FussballerUpdateModel):
    """Pydantic-Model für die Fussballer-Daten."""

    adresse: AdresseModel
    """Die Adresse des Fussballers."""
    auszeichnungen: list[AuszeichnungModel]
    """Die Liste der Auszeichnungen des Fussballers."""
    username: Annotated[str, StringConstraints(max_length=20)]
    """Der Benutzername für Login."""

    def to_fussballer(self) -> Fussballer:
        """Konvertierung in ein Fussballer-Objekt für SQLAlchemy.

        :return: Fussballer-Objekt für SQLAlchemy
        :rtype: Fussballer
        """
        fussballer_dict: dict[str, Any] = self.to_dict()
        fussballer_dict["username"] = self.username

        fussballer: Final = Fussballer(**fussballer_dict)
        fussballer.adresse: Adresse = self.adresse.to_adresse()
        fussballer.auszeichnungen: list[Auszeichnung] = [
            auszeichnung_model.to_auszeichnung()
            for auszeichnung_model in self.auszeichnungen
        ]
        return fussballer
