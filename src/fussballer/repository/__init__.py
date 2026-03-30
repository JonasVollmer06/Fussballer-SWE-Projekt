"""Modul für den DB-Zugriff."""

from fussballer.repository.session_factory import Session, engine

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "Session",
    "engine",
]
