"""Tests d'integration reseau : Sets, Rulings, Catalogs, Bulk Data + erreur 404."""

from __future__ import annotations

import pytest

from baobab_scryfall_api_caller import ScryfallApiCaller
from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData
from baobab_scryfall_api_caller.models.catalogs.catalog import Catalog
from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.models.rulings.ruling import Ruling
from baobab_scryfall_api_caller.models.sets.set import Set

from tests.integration.scryfall_live_constants import (
    BULK_TYPE_ORACLE_CARDS_SLUG,
    CATALOG_KEY_CREATURE_TYPES,
    DOC_EXAMPLE_CARD_ID,
    KNOWN_SET_CODE,
)

pytestmark = pytest.mark.integration


class TestScryfallLiveSets:
    """Liste et acces unitaire set."""

    def test_list_sets_returns_list_response(self, live_scryfall_client: ScryfallApiCaller) -> None:
        """GET /sets — au moins un set, structure paginee."""
        page = live_scryfall_client.sets.list_sets()
        assert isinstance(page, ListResponse)
        assert len(page.data) >= 1
        assert isinstance(page.data[0], Set)
        assert page.data[0].code

    def test_get_by_code_returns_set(self, live_scryfall_client: ScryfallApiCaller) -> None:
        """GET /sets/{code} — set connu stable."""
        set_obj = live_scryfall_client.sets.get_by_code(KNOWN_SET_CODE)
        assert isinstance(set_obj, Set)
        assert set_obj.code == KNOWN_SET_CODE

    def test_get_by_id_matches_get_by_code(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """GET /sets/{id} — coherence avec le meme set obtenu par code (pas d'UUID fige)."""
        by_code = live_scryfall_client.sets.get_by_code(KNOWN_SET_CODE)
        by_id = live_scryfall_client.sets.get_by_id(by_code.id)
        assert isinstance(by_id, Set)
        assert by_id.id == by_code.id
        assert by_id.code == KNOWN_SET_CODE


class TestScryfallLiveRulings:
    """Rulings pour une carte connue."""

    def test_list_for_card_id_structure(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """GET /cards/:id/rulings — reponse liste coherente (liste eventuellement vide)."""
        page = live_scryfall_client.rulings.list_for_card_id(DOC_EXAMPLE_CARD_ID)
        assert isinstance(page, ListResponse)
        for item in page.data:
            assert isinstance(item, Ruling)


class TestScryfallLiveCatalogs:
    """Catalogue des noms de cartes."""

    def test_get_card_names_returns_catalog(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """GET /catalog/card-names — valeurs non vides."""
        catalog = live_scryfall_client.catalogs.get_card_names()
        assert isinstance(catalog, Catalog)
        assert catalog.catalog_key == "card-names"
        assert catalog.uri.startswith("http")
        assert catalog.total_values >= 0
        assert len(catalog.values) >= 1

    def test_get_catalog_creature_types(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """GET /catalog/{key} — acces generique (cle stable)."""
        catalog = live_scryfall_client.catalogs.get_catalog(CATALOG_KEY_CREATURE_TYPES)
        assert isinstance(catalog, Catalog)
        assert catalog.catalog_key == CATALOG_KEY_CREATURE_TYPES
        assert catalog.total_values >= 0


class TestScryfallLiveBulkData:
    """Metadonnees bulk."""

    def test_list_bulk_datasets_returns_entries(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """GET /bulk-data — liste non vide, champs structurants."""
        page = live_scryfall_client.bulk_data.list_bulk_datasets()
        assert isinstance(page, ListResponse)
        assert len(page.data) >= 1
        first = page.data[0]
        assert isinstance(first, BulkData)
        assert first.id
        assert first.download_uri.startswith("http")

    def test_get_by_type_oracle_cards(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """GET /bulk-data/{type} — jeu courant documente Scryfall."""
        bulk = live_scryfall_client.bulk_data.get_by_type(BULK_TYPE_ORACLE_CARDS_SLUG)
        assert isinstance(bulk, BulkData)
        assert bulk.id
        assert bulk.download_uri.startswith("http")
        assert bulk.type == "oracle_cards"

    def test_get_by_id_matches_first_list_entry(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """GET /bulk-data/{id} — coherence avec la liste (pas d'UUID fige)."""
        page = live_scryfall_client.bulk_data.list_bulk_datasets()
        first = page.data[0]
        again = live_scryfall_client.bulk_data.get_by_id(first.id)
        assert isinstance(again, BulkData)
        assert again.id == first.id


class TestScryfallLiveErrorPaths:
    """Erreurs metier attendues sur reponses Scryfall."""

    def test_get_by_id_unknown_uuid_raises_not_found(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """UUID inexistant — 404 mappe en ScryfallNotFoundException."""
        unknown = "00000000-0000-0000-0000-000000000000"
        try:
            live_scryfall_client.cards.get_by_id(unknown)
        except ScryfallNotFoundException as exc:
            assert exc.http_status == 404
        else:
            pytest.fail("expected ScryfallNotFoundException")

    def test_get_named_without_exact_or_fuzzy_raises_validation(
        self,
        live_scryfall_client: ScryfallApiCaller,
    ) -> None:
        """Validation locale — aucun appel HTTP (named exige exact ou fuzzy)."""
        with pytest.raises(ScryfallValidationException):
            live_scryfall_client.cards.get_named()
