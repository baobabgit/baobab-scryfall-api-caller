"""Tests du modele Ruling."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from baobab_scryfall_api_caller.models.rulings.ruling import Ruling


class TestRuling:
    """Valide le modele de donnees Ruling."""

    def test_equality(self) -> None:
        """Deux instances identiques doivent etre egales."""
        first = Ruling(
            oracle_id="a",
            source="wotc",
            published_at="2007-02-01",
            comment="x",
        )
        second = Ruling(
            oracle_id="a",
            source="wotc",
            published_at="2007-02-01",
            comment="x",
        )
        assert first == second

    def test_immutability(self) -> None:
        """Le modele doit etre immuable (frozen)."""
        instance = Ruling(
            oracle_id="a",
            source="wotc",
            published_at="2007-02-01",
            comment="x",
        )
        with pytest.raises(FrozenInstanceError):
            instance.comment = "y"  # type: ignore[misc]

    def test_empty_comment_allowed(self) -> None:
        """Le commentaire peut etre une chaine vide."""
        instance = Ruling(
            oracle_id="a",
            source="wotc",
            published_at="2007-02-01",
            comment="",
        )
        assert instance.comment == ""
