"""Einfache Tests mit pytest."""

from pytest import mark


@mark.simple
def test_simple() -> None:
    assert True


@mark.skip(reason="Fail")
def test_always_fail() -> None:
    assert not True
