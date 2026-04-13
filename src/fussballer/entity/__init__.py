"""Modul für persistente Patientendaten."""

from fussballer.entity.adresse import Adresse
from fussballer.entity.auszeichnung import Auszeichnung
from fussballer.entity.base import Base
from fussballer.entity.fussballer import Fussballer
from fussballer.entity.position import Position

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "Adresse",
    "Auszeichnung",
    "Base",
    "Fussballer",
    "Position",
]
