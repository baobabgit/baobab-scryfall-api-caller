"""Tests du telechargeur bulk (mocks, sans reseau)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from baobab_web_api_caller.exceptions.transport_exception import TransportException
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory

from baobab_scryfall_api_caller.exceptions import (
    ScryfallBulkDataException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData
from baobab_scryfall_api_caller.services.bulk_data.bulk_dataset_downloader import (
    BulkDatasetDownloader,
)


def _sample_bulk_data() -> BulkData:
    return BulkData(
        id="11111111-1111-4111-8111-111111111111",
        uri="https://api.scryfall.com/bulk-data/11111111-1111-4111-8111-111111111111",
        type="oracle_cards",
        name="Oracle Cards",
        description="Desc",
        download_uri="https://data.scryfall.io/oracle-cards/oracle-cards.json",
        updated_at="2020-01-01",
        size=500,
        content_type="application/json",
        content_encoding="gzip",
    )


class TestBulkDatasetDownloader:
    """Scenarios unitaires avec BulkFileDownloader simule."""

    def test_destination_must_be_file_not_directory(self, tmp_path: Path) -> None:
        """Un repertoire existant comme cible est refuse."""
        d = tmp_path / "dir"
        d.mkdir()
        downloader = BulkDatasetDownloader(session_factory=RequestsSessionFactory())
        try:
            downloader.download(
                bulk_data=_sample_bulk_data(),
                destination_path=d,
                overwrite=False,
            )
        except ScryfallValidationException as exc:
            assert "directory" in exc.message.lower()
        else:
            assert False, "Expected ScryfallValidationException"

    def test_chunk_size_positive(self) -> None:
        """chunk_size <= 0 invalide."""
        downloader = BulkDatasetDownloader(session_factory=RequestsSessionFactory())
        with pytest.raises(ScryfallValidationException):
            downloader.download(
                bulk_data=_sample_bulk_data(),
                destination_path=Path("/tmp/x.json"),
                chunk_size=0,
            )

    @patch(
        "baobab_scryfall_api_caller.services.bulk_data.bulk_dataset_downloader.BulkFileDownloader"
    )
    def test_download_delegates_and_returns_result(
        self, mock_bfd_class: MagicMock, tmp_path: Path
    ) -> None:
        """Le downloader baobab est appele et le chemin est propage."""
        out = tmp_path / "out.json"
        mock_instance = MagicMock()
        mock_instance.download.return_value = out
        mock_bfd_class.from_service_config.return_value = mock_instance

        bd = BulkDatasetDownloader(session_factory=RequestsSessionFactory())
        result = bd.download(bulk_data=_sample_bulk_data(), destination_path=out, overwrite=True)

        assert result.path == out
        assert result.bulk_data.id == _sample_bulk_data().id
        mock_instance.download.assert_called_once()
        call_kw = mock_instance.download.call_args[1]
        assert call_kw["output_path"] == out
        assert call_kw["overwrite"] is True

    @patch(
        "baobab_scryfall_api_caller.services.bulk_data.bulk_dataset_downloader.BulkFileDownloader"
    )
    def test_transport_exception_maps_to_bulk_data_exception(
        self,
        mock_bfd_class: MagicMock,
        tmp_path: Path,
    ) -> None:
        """TransportException (ex. fichier existant) enveloppee."""
        mock_instance = MagicMock()
        mock_instance.download.side_effect = TransportException("output_path already exists")
        mock_bfd_class.from_service_config.return_value = mock_instance

        bd = BulkDatasetDownloader(session_factory=RequestsSessionFactory())
        dest = tmp_path / "f.json"
        try:
            bd.download(bulk_data=_sample_bulk_data(), destination_path=dest, overwrite=False)
        except ScryfallBulkDataException as exc:
            assert "Bulk download failed" in exc.message
            assert exc.cause is not None
        else:
            assert False, "Expected ScryfallBulkDataException"
