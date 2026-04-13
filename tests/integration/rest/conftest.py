"""Fixture für pytest: Neuladen der Datenbank."""

from common_test import check_readiness, db_populate, keycloak_populate
from pytest import fixture

session_scope = "session"

@fixture(scope=session_scope, autouse=True)
def check_readiness_per_session() -> None:
    check_readiness()
    print("Appserver ist 'bereit'")

