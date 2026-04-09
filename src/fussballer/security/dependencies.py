"""Factory-Funktionen für den Zugriff auf Services mittels Dependency Injection."""

from patient.security.token_service import TokenService
from patient.security.user_service import UserService

"""Erstellen eines einzigen Objektes TokenService (Singleton)"""
_token_service = TokenService()


def get_token_service() -> TokenService:
    """Übergeben des erstellten Objektes (TokenService)."""
    return _token_service


_user_service = UserService()


def get_user_service() -> UserService:
    """Übergeben des erstellten Objektes (UserService)."""
    return _user_service
