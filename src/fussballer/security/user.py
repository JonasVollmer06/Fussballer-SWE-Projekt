"""Entity-Klasse für Benutzer."""

from dataclasses import dataclass

from fussballer.security.role import Role


@dataclass()
class User:
    """Entity-Klasse für Benutzer."""

    username: str
    email: str
    nachname: str
    vorname: str
    roles: list[Role]
    password: str | None = None
