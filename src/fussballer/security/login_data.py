"""Eine Datenklasse für die Anmeldedaten für Keycloak."""

from dataclasses import dataclass

__all__ = ["LoginData"]


@dataclass
class LoginData:
    """Datenklasse für Keycloak Anmeldedaten."""

    username: str

    password: str

    class Config:
        """Konfigurationsklasse für die LoginData-Klasse."""

        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "p",   # NOSONAR
            },
        }
