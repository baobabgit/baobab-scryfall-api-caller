"""Tests du mapper BulkDataMapper."""

from __future__ import annotations

from typing import Any

import pytest

from baobab_scryfall_api_caller.exceptions import (
    ScryfallBulkDataException,
    ScryfallResponseFormatException,
)
from baobab_scryfall_api_caller.mappers.bulk_data_mapper import BulkDataMapper
from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData


def _valid_bulk_payload(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "object": "bulk_data",
        "id": "922288cb-4bef-45e1-bb30-0c2bd3d3534f",
        "uri": "https://api.scryfall.com/bulk-data/922288cb-4bef-45e1-bb30-0c2bd3d3534f",
        "type": "oracle_cards",
        "name": "Oracle Cards",
        "description": "One card per oracle id.",
        "download_uri": "https://data.scryfall.io/oracle-cards/oracle-cards.json",
        "updated_at": "2020-01-01T00:00:00.000Z",
        "size": 1024,
        "content_type": "application/json",
        "content_encoding": "gzip",
    }
    base.update(overrides)
    return base


class TestBulkDataMapper:
    """Valide le mapping des payloads bulk_data."""

    def test_map_bulk_data_nominal(self) -> None:
        """Un payload valide doit produire un BulkData."""
        mapper = BulkDataMapper()
        payload = _valid_bulk_payload()
        result = mapper.map_bulk_data(payload)
        assert isinstance(result, BulkData)
        assert result.id == payload["id"]
        assert result.download_uri == payload["download_uri"]
        assert result.size == 1024

    def test_map_bulk_data_rejects_non_dict(self) -> None:
        """Un type non dict doit lever une erreur de format."""
        mapper = BulkDataMapper()
        try:
            mapper.map_bulk_data([])
        except ScryfallResponseFormatException as exception:
            assert "dictionary" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_bulk_data_wrong_object(self) -> None:
        """Un objet autre que bulk_data doit etre rejete."""
        mapper = BulkDataMapper()
        payload = _valid_bulk_payload(object="list")
        try:
            mapper.map_bulk_data(payload)
        except ScryfallResponseFormatException as exception:
            assert "object" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_bulk_data_invalid_download_scheme(self) -> None:
        """Une URI de telechargement non HTTP(S) doit lever une erreur metier bulk."""
        mapper = BulkDataMapper()
        payload = _valid_bulk_payload(download_uri="ftp://example.com/file.json")
        try:
            mapper.map_bulk_data(payload)
        except ScryfallBulkDataException as exception:
            assert "HTTP(S)" in exception.message
        else:
            assert False, "Expected ScryfallBulkDataException"

    def test_map_bulk_data_zero_size(self) -> None:
        """Une taille nulle doit etre rejetee comme incoherente."""
        mapper = BulkDataMapper()
        payload = _valid_bulk_payload(size=0)
        try:
            mapper.map_bulk_data(payload)
        except ScryfallBulkDataException as exception:
            assert "positive" in exception.message
        else:
            assert False, "Expected ScryfallBulkDataException"

    def test_map_bulk_data_missing_field(self) -> None:
        """Un champ obligatoire manquant doit lever une erreur de format."""
        mapper = BulkDataMapper()
        payload = _valid_bulk_payload()
        del payload["content_encoding"]
        try:
            mapper.map_bulk_data(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_bulk_data_http_download_uri_accepted(self) -> None:
        """Une URI http (non TLS) reste acceptee si absolue."""
        mapper = BulkDataMapper()
        payload = _valid_bulk_payload(download_uri="http://data.scryfall.io/x.json")
        result = mapper.map_bulk_data(payload)
        assert result.download_uri.startswith("http://")

    @pytest.mark.parametrize(
        "overrides",
        [
            pytest.param({"id": ""}, id="empty_id"),
            pytest.param({"id": 99}, id="id_not_str"),
            pytest.param({"uri": ""}, id="empty_uri"),
            pytest.param({"type": ""}, id="empty_type"),
            pytest.param({"name": ""}, id="empty_name"),
            pytest.param({"description": None}, id="description_not_str"),
            pytest.param({"download_uri": "  "}, id="download_uri_blank"),
            pytest.param({"updated_at": ""}, id="empty_updated_at"),
            pytest.param({"size": -2}, id="negative_size"),
            pytest.param({"size": "large"}, id="size_not_int"),
            pytest.param({"content_type": ""}, id="empty_content_type"),
            pytest.param({"content_encoding": ""}, id="empty_content_encoding"),
        ],
    )
    def test_map_bulk_data_invalid_required_fields(
        self,
        overrides: dict[str, Any],
    ) -> None:
        """Chaque champ obligatoire invalide doit produire ScryfallResponseFormatException."""
        mapper = BulkDataMapper()
        payload = _valid_bulk_payload(**overrides)
        try:
            mapper.map_bulk_data(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
