"""Modul Deklaration."""

from fussballer.asgi_server import run
from fussballer.fastapi_app import app

__all__ = ["app", "main"]


def main():  # noqa: RUF067
    """main-Funktion, damit das Modul als Skript aufgerufen werden kann."""
    run()
