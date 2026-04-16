"""Modul für den DB-Zugriff."""

from fussballer.repository.fussballer_repository import FussballerRepository
from fussballer.repository.pageable import Pageable
from fussballer.repository.session_factory import Session, engine
from fussballer.repository.slice import Slice

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "FussballerRepository",
    "Pageable",
    "Session",
    "Slice",
    "engine",
]
