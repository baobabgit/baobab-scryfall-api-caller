"""Tests du service metier BulkDataService."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from baobab_scryfall_api_caller.exceptions import (
    ScryfallNotFoundException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData
from baobab_scryfall_api_caller.services.bulk_data.bulk_data_service import BulkDataService
from baobab_scryfall_api_caller.services.bulk_data.bulk_dataset_downloader import (
    BulkDatasetDownloader,
)
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


def _bulk_item(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "object": "bulk_data",
        "id": "11111111-1111-4111-8111-111111111111",
        "uri": "https://api.scryfall.com/bulk-data/11111111-1111-4111-8111-111111111111",
        "type": "oracle_cards",
        "name": "Oracle Cards",
        "description": "Desc",
        "download_uri": "https://data.scryfall.io/oracle-cards/oracle-cards.json",
        "updated_at": "2020-01-01",
        "size": 500,
        "content_type": "application/json",
        "content_encoding": "gzip",
    }
    base.update(overrides)
    return base


class FakeWebApiCaller:
    """Simule baobab-web-api-caller pour BulkDataService."""

    def __init__(self, *, response: Any = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.calls: list[dict[str, Any]] = []

    def get(self, *, route: str, params: dict[str, Any] | None, headers: dict[str, str]) -> Any:
        """Enregistre l'appel et retourne la reponse configuree."""
        self.calls.append({"route": route, "params": params, "headers": headers})
        if self.error is not None:
            raise self.error
        return self.response


class TestBulkDataService:
    """Scenarios liste, get par id/type, validation et erreurs."""

    def test_list_bulk_datasets_nominal(self) -> None:
        """Listage nominal des jeux bulk."""
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [_bulk_item(), _bulk_item(id="22222222-2222-4222-8222-222222222222")],
        }
        caller = FakeWebApiCaller(response=list_payload)
        service = BulkDataService(web_api_caller=caller)
        result = service.list_bulk_datasets()
        assert len(result.data) == 2
        assert all(isinstance(item, BulkData) for item in result.data)
        assert caller.calls[0]["route"] == "/bulk-data"

    def test_list_bulk_datasets_empty(self) -> None:
        """Liste vide de jeux bulk."""
        list_payload = {"object": "list", "has_more": False, "data": []}
        caller = FakeWebApiCaller(response=list_payload)
        service = BulkDataService(web_api_caller=caller)
        result = service.list_bulk_datasets()
        assert result.data == []

    def test_get_by_id_nominal(self) -> None:
        """Recuperation par UUID."""
        uid = "11111111-1111-4111-8111-111111111111"
        caller = FakeWebApiCaller(response=_bulk_item())
        service = BulkDataService(web_api_caller=caller)
        result = service.get_by_id(uid.upper())
        assert result.id == uid
        assert caller.calls[0]["route"] == f"/bulk-data/{uid}"

    def test_get_by_type_nominal(self) -> None:
        """Recuperation par type kebab-case d'URL."""
        caller = FakeWebApiCaller(response=_bulk_item())
        service = BulkDataService(web_api_caller=caller)
        result = service.get_by_type(" ORACLE-CARDS ")
        assert caller.calls[0]["route"] == "/bulk-data/oracle-cards"
        assert isinstance(result, BulkData)

    def test_validation_bulk_type_invalid(self) -> None:
        """Un type bulk mal formate doit etre rejete."""
        caller = FakeWebApiCaller(response=_bulk_item())
        service = BulkDataService(web_api_caller=caller)
        try:
            service.get_by_type("bad_type")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_bulk_type_whitespace_only(self) -> None:
        """Un type bulk vide apres normalisation doit etre rejete."""
        caller = FakeWebApiCaller(response=_bulk_item())
        service = BulkDataService(web_api_caller=caller)
        try:
            service.get_by_type("   ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_bulk_type_not_string(self) -> None:
        """Un type bulk non chaine doit etre rejete."""
        caller = FakeWebApiCaller(response=_bulk_item())
        service = BulkDataService(web_api_caller=caller)
        try:
            service.get_by_type(1)  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_bulk_type_too_long(self) -> None:
        """Un slug type trop long doit etre rejete."""
        caller = FakeWebApiCaller(response=_bulk_item())
        service = BulkDataService(web_api_caller=caller)
        long_slug = "a" * 81
        try:
            service.get_by_type(long_slug)
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_validation_bulk_data_id_invalid(self) -> None:
        """Un UUID invalide pour get_by_id doit etre rejete."""
        caller = FakeWebApiCaller(response=_bulk_item())
        service = BulkDataService(web_api_caller=caller)
        try:
            service.get_by_id("not-uuid")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_not_found(self) -> None:
        """Un 404 HTTP doit produire ScryfallNotFoundException."""
        caller = FakeWebApiCaller(
            response={"object": "error", "status": 404, "details": "Not found"},
        )
        service = BulkDataService(web_api_caller=caller)
        try:
            service.get_by_type("oracle-cards")
        except ScryfallNotFoundException:
            assert True
        else:
            assert False, "Expected ScryfallNotFoundException"

    def test_transport_error(self) -> None:
        """Une erreur transport doit etre traduite."""
        caller = FakeWebApiCaller(error=RuntimeError("network"))
        service = BulkDataService(web_api_caller=caller)
        try:
            service.list_bulk_datasets()
        except ScryfallRequestException as exception:
            assert "network" in exception.message
        else:
            assert False, "Expected ScryfallRequestException"

    def test_malformed_list_response(self) -> None:
        """Une reponse liste invalide doit lever une erreur de format."""
        caller = FakeWebApiCaller(response={"object": "catalog", "data": []})
        service = BulkDataService(web_api_caller=caller)
        try:
            service.list_bulk_datasets()
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_list_item_mapping_failure(self) -> None:
        """Un element de liste invalide doit echouer au mapping."""
        list_payload = {
            "object": "list",
            "has_more": False,
            "data": [_bulk_item(object="card")],
        }
        caller = FakeWebApiCaller(response=list_payload)
        service = BulkDataService(web_api_caller=caller)
        try:
            service.list_bulk_datasets()
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_download_without_downloader_raises(self) -> None:
        """Sans BulkDatasetDownloader, download_bulk_dataset doit etre refuse."""
        caller = FakeWebApiCaller(response=_bulk_item())
        service = BulkDataService(web_api_caller=caller)
        meta = service.get_by_type("oracle-cards")
        try:
            service.download_bulk_dataset(bulk_data=meta, destination_path=Path("/tmp/x.json"))
        except ScryfallValidationException as exc:
            assert "BulkDatasetDownloader" in exc.message
        else:
            assert False, "Expected ScryfallValidationException"

    @patch(
        "baobab_scryfall_api_caller.services.bulk_data.bulk_dataset_downloader.BulkFileDownloader"
    )
    def test_download_with_downloader_delegates(self, mock_bfd: MagicMock, tmp_path: Path) -> None:
        """Avec downloader injecte, la delegation vers baobab est effectuee."""
        mock_inst = MagicMock()
        out = tmp_path / "out.json"
        mock_inst.download.return_value = out
        mock_bfd.from_service_config.return_value = mock_inst

        caller = FakeWebApiCaller(response=_bulk_item())
        bd = BulkDatasetDownloader(session_factory=RequestsSessionFactory())
        service = BulkDataService(web_api_caller=caller, bulk_dataset_downloader=bd)
        meta = service.get_by_type("oracle-cards")
        result = service.download_bulk_dataset(bulk_data=meta, destination_path=out)

        assert result.path == out
        assert result.bulk_data.id == meta.id
        mock_inst.download.assert_called_once()

    @patch(
        "baobab_scryfall_api_caller.services.bulk_data.bulk_dataset_downloader.BulkFileDownloader"
    )
    def test_download_by_type_fetches_then_downloads(
        self, mock_bfd: MagicMock, tmp_path: Path
    ) -> None:
        """download_bulk_dataset_by_type enchaine get_by_type et download."""
        mock_inst = MagicMock()
        out = tmp_path / "f.json"
        mock_inst.download.return_value = out
        mock_bfd.from_service_config.return_value = mock_inst

        caller = FakeWebApiCaller(response=_bulk_item())
        bd = BulkDatasetDownloader(session_factory=RequestsSessionFactory())
        service = BulkDataService(web_api_caller=caller, bulk_dataset_downloader=bd)
        result = service.download_bulk_dataset_by_type("oracle-cards", destination_path=out)

        assert result.path == out
        assert caller.calls[-1]["route"] == "/bulk-data/oracle-cards"
