"""Exceptions für die Security-Klassen."""


class LoginError(Exception):
    """Klasse für Exceptions bei fehlerhaften Anmeldedaten."""

    def __init__(self, username: str | None = None) -> None:
        """Konstruktor der Exception-Klasse LoginError."""
        super().__init__(f"Fehlerhafte Benutzerdaten fuer {username}")
        self.username = username


class AuthorizationError(Exception):
    """Exception falls der extrahierte Token aus dem Request-Header fehlerhaft ist."""
