"""Tests du mapper CatalogMapper."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.catalog_mapper import CatalogMapper
from baobab_scryfall_api_caller.models.catalogs.catalog import Catalog


def _valid_catalog_payload(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "object": "catalog",
        "uri": "https://api.scryfall.com/catalog/card-names",
        "total_values": 2,
        "data": ["Alpha", "Beta"],
    }
    base.update(overrides)
    return base


class TestCatalogMapper:
    """Valide le mapping des payloads catalogue."""

    def test_map_catalog_nominal(self) -> None:
        """Un payload valide doit produire un Catalog."""
        mapper = CatalogMapper()
        payload = _valid_catalog_payload()
        result = mapper.map_catalog(payload, catalog_key="card-names")
        assert isinstance(result, Catalog)
        assert result.catalog_key == "card-names"
        assert result.total_values == 2
        assert result.values == ("Alpha", "Beta")

    def test_map_catalog_empty_data(self) -> None:
        """Une liste vide doit etre acceptee."""
        mapper = CatalogMapper()
        payload = _valid_catalog_payload(total_values=0, data=[])
        result = mapper.map_catalog(payload, catalog_key="x")
        assert result.values == ()

    def test_map_catalog_rejects_non_dict(self) -> None:
        """Un type non dict doit lever une erreur de format."""
        mapper = CatalogMapper()
        try:
            mapper.map_catalog("bad", catalog_key="x")
        except ScryfallResponseFormatException as exception:
            assert "dictionary" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_catalog_wrong_object(self) -> None:
        """Un objet autre que catalog doit etre rejete."""
        mapper = CatalogMapper()
        payload = _valid_catalog_payload(object="list")
        try:
            mapper.map_catalog(payload, catalog_key="x")
        except ScryfallResponseFormatException as exception:
            assert "object" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_catalog_invalid_uri(self) -> None:
        """Une URI manquante doit etre rejetee."""
        mapper = CatalogMapper()
        payload = _valid_catalog_payload(uri="")
        try:
            mapper.map_catalog(payload, catalog_key="x")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_catalog_invalid_total_values(self) -> None:
        """Un total_values invalide doit etre rejete."""
        mapper = CatalogMapper()
        payload = _valid_catalog_payload(total_values=-1)
        try:
            mapper.map_catalog(payload, catalog_key="x")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_catalog_total_values_wrong_type(self) -> None:
        """Un total_values non entier doit etre rejete."""
        mapper = CatalogMapper()
        payload = _valid_catalog_payload(total_values="10")
        try:
            mapper.map_catalog(payload, catalog_key="x")
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_catalog_data_not_list(self) -> None:
        """Le champ data doit etre une liste."""
        mapper = CatalogMapper()
        payload = _valid_catalog_payload(data="not-a-list")
        try:
            mapper.map_catalog(payload, catalog_key="x")
        except ScryfallResponseFormatException as exception:
            assert "data" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_catalog_non_string_entry(self) -> None:
        """Une entree non textuelle dans data doit etre rejetee."""
        mapper = CatalogMapper()
        payload = _valid_catalog_payload(data=["ok", 1], total_values=2)
        try:
            mapper.map_catalog(payload, catalog_key="x")
        except ScryfallResponseFormatException as exception:
            assert "index" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"
