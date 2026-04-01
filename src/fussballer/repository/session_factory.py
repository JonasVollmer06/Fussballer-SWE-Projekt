"""Asynchrone Engine und die Factory für asynchrone Sessions konfigurieren."""

from typing import Final

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fussballer.config.db import (
    db_connect_args,
    db_log_statements,
    db_url,
)

__all__ = ["Session", "engine"]

engine: Final = create_engine(
    db_url,
    connect_args=db_connect_args,
    echo=db_log_statements,
)
"""Hier haben wir eine Enige für SQLAlchemy, mit dem Zweck DB-Verbindungen und den
dazugehörigen Sessions zu erstellen Die Engine entspricht somit einer Verbindung bzw.
Schnittstelle zur Datenbank.
"""

Session = sessionmaker(bind=engine, autoflush=False)
"""Factory für Sessions, um generierte SQL-Anweisungen in Transaktionen abzusetzen.
Mithilfe des Objekts Session können also später Datenbank-Sessions erzeugt werden.
"""
