"""Tests du decoupage d'URL pour BulkFileDownloader."""

from __future__ import annotations

from baobab_web_api_caller.core.http_method import HttpMethod

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.services.bulk_data.bulk_download_uri import (
    build_service_config_and_request_for_bulk_download,
)


class TestBulkDownloadUri:
    """Validation de la construction ServiceConfig + BaobabRequest."""

    def test_https_data_host(self) -> None:
        """URL standard Scryfall (CDN)."""
        url = "https://data.scryfall.io/oracle-cards/oracle-cards.json"
        cfg, req = build_service_config_and_request_for_bulk_download(url)
        assert cfg.base_url == "https://data.scryfall.io"
        assert req.method == HttpMethod.GET
        assert req.path == "/oracle-cards/oracle-cards.json"
        assert req.query_params == {}

    def test_query_string(self) -> None:
        """Parametres de requete repartis dans le modele Baobab."""
        url = "https://example.com/path/file.bin?x=1&y=two"
        cfg, req = build_service_config_and_request_for_bulk_download(url)
        assert cfg.base_url == "https://example.com"
        assert req.path == "/path/file.bin"
        assert dict(req.query_params) == {"x": "1", "y": "two"}

    def test_empty_uri(self) -> None:
        """Chaine vide rejetee."""
        try:
            build_service_config_and_request_for_bulk_download("   ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_not_http(self) -> None:
        """Schema non supporte."""
        try:
            build_service_config_and_request_for_bulk_download("ftp://x/y")
        except ScryfallValidationException as exc:
            assert "http" in exc.message.lower()
        else:
            assert False, "Expected ScryfallValidationException"

    def test_default_headers_merge(self) -> None:
        """Headers par defaut transmis au ServiceConfig."""
        url = "https://data.scryfall.io/a.json"
        cfg, _ = build_service_config_and_request_for_bulk_download(
            url,
            default_headers={"User-Agent": "test"},
        )
        assert cfg.default_headers["User-Agent"] == "test"
