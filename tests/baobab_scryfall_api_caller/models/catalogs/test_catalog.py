"""Tests du modele Catalog."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from baobab_scryfall_api_caller.models.catalogs.catalog import Catalog


class TestCatalog:
    """Valide le modele de donnees Catalog."""

    def test_equality(self) -> None:
        """Deux instances identiques doivent etre egales."""
        first = Catalog(
            catalog_key="x",
            uri="https://example.com",
            total_values=1,
            values=("a",),
        )
        second = Catalog(
            catalog_key="x",
            uri="https://example.com",
            total_values=1,
            values=("a",),
        )
        assert first == second

    def test_immutability(self) -> None:
        """Le modele doit etre immuable (frozen)."""
        instance = Catalog(
            catalog_key="x",
            uri="https://example.com",
            total_values=0,
            values=(),
        )
        with pytest.raises(FrozenInstanceError):
            instance.uri = "y"  # type: ignore[misc]

    def test_empty_values_tuple(self) -> None:
        """Un catalogue peut ne contenir aucune valeur."""
        instance = Catalog(
            catalog_key="empty",
            uri="https://example.com",
            total_values=0,
            values=(),
        )
        assert instance.values == ()
