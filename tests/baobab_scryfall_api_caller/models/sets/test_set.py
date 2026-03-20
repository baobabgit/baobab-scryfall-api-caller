"""Tests du modele Set."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from baobab_scryfall_api_caller.models.sets.set import Set


class TestSet:
    """Valide le modele de donnees Set."""

    def test_frozen_dataclass_equality(self) -> None:
        """Deux instances identiques doivent etre egales."""
        first = Set(id="a", code="neo", name="Neo")
        second = Set(id="a", code="neo", name="Neo")
        assert first == second

    def test_immutability(self) -> None:
        """Le modele doit etre immuable (frozen)."""
        instance = Set(id="a", code="neo", name="Neo")
        with pytest.raises(FrozenInstanceError):
            instance.name = "Other"  # type: ignore[misc]
