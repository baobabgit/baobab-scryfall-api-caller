"""Tests du modele BulkData."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData


class TestBulkData:
    """Valide le modele de donnees BulkData."""

    def test_equality(self) -> None:
        """Deux instances identiques doivent etre egales."""
        first = _sample_bulk_data()
        second = _sample_bulk_data()
        assert first == second

    def test_immutability(self) -> None:
        """Le modele doit etre immuable (frozen)."""
        instance = _sample_bulk_data()
        with pytest.raises(FrozenInstanceError):
            instance.size = 0  # type: ignore[misc]

    def test_download_uri_exposed(self) -> None:
        """L'URL de telechargement doit etre accessible."""
        instance = _sample_bulk_data()
        assert instance.download_uri.startswith("https://")


def _sample_bulk_data() -> BulkData:
    return BulkData(
        id="922288cb-4bef-45e1-bb30-0c2bd3d3534f",
        uri="https://api.scryfall.com/bulk-data/922288cb-4bef-45e1-bb30-0c2bd3d3534f",
        type="all_cards",
        name="All Cards",
        description="Every card on Scryfall.",
        download_uri="https://data.scryfall.io/all-cards/all-cards.json",
        updated_at="2019-01-01",
        size=100,
        content_type="application/json",
        content_encoding="gzip",
    )
