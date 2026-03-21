"""Service metier Bulk Data (metadonnees des exports Scryfall)."""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from baobab_scryfall_api_caller.cache.json_response_cache import JsonResponseCache
from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.mappers.bulk_data_mapper import BulkDataMapper
from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData
from baobab_scryfall_api_caller.models.bulk_data.bulk_download_result import BulkDownloadResult
from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.pagination.scryfall_list_response_parser import (
    ScryfallListResponseParser,
)
from baobab_scryfall_api_caller.services.bulk_data.bulk_data_api_client import BulkDataApiClient
from baobab_scryfall_api_caller.services.bulk_data.bulk_dataset_downloader import (
    BulkDatasetDownloader,
)
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)

_BULK_TYPE_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_MAX_BULK_TYPE_LEN = 80


class BulkDataService:
    """Expose les operations Bulk Data V1 (liste, metadonnees et telechargement optionnel)."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        api_client: BulkDataApiClient | None = None,
        bulk_data_mapper: BulkDataMapper | None = None,
        list_parser: ScryfallListResponseParser | None = None,
        response_cache: JsonResponseCache | None = None,
        cacheable_get_predicate: Callable[[str, dict[str, Any] | None], bool] | None = None,
        bulk_dataset_downloader: BulkDatasetDownloader | None = None,
    ) -> None:
        """Initialise le service Bulk Data avec ses dependances."""
        self.api_client = api_client or BulkDataApiClient(
            web_api_caller=web_api_caller,
            response_cache=response_cache,
            cacheable_get_predicate=cacheable_get_predicate,
        )
        self.bulk_data_mapper = bulk_data_mapper or BulkDataMapper()
        self.list_parser = list_parser or ScryfallListResponseParser()
        self._bulk_dataset_downloader = bulk_dataset_downloader

    def list_bulk_datasets(self) -> ListResponse[BulkData]:
        """Liste tous les jeux de donnees bulk disponibles (`GET /bulk-data`)."""
        payload = self.api_client.get(route="/bulk-data")
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.bulk_data_mapper.map_bulk_data,
        )

    def get_by_id(self, bulk_data_id: str) -> BulkData:
        """Recupere les metadonnees d'un jeu bulk par identifiant UUID.

        :param bulk_data_id: UUID du jeu (``GET /bulk-data/{id}``).
        """
        normalized = ScryfallRequestValidators.require_uuid_string(
            value=bulk_data_id,
            field_name="bulk_data_id",
        )
        payload = self.api_client.get(route=f"/bulk-data/{normalized}")
        return self.bulk_data_mapper.map_bulk_data(payload)

    def get_by_type(self, bulk_type: str) -> BulkData:
        """Recupere les metadonnees d'un jeu bulk par type d'URL Scryfall.

        :param bulk_type: Segment de chemin kebab-case (ex. ``oracle-cards``),
            tel que dans ``GET /bulk-data/{type}``.
        """
        normalized = self._require_bulk_type_slug(bulk_type=bulk_type)
        payload = self.api_client.get(route=f"/bulk-data/{normalized}")
        return self.bulk_data_mapper.map_bulk_data(payload)

    @staticmethod
    def _require_bulk_type_slug(*, bulk_type: str) -> str:
        if not isinstance(bulk_type, str):
            raise ScryfallValidationException(
                "'bulk_type' must be a string.",
                params={"bulk_type": bulk_type},
            )
        normalized = bulk_type.strip().lower()
        if not normalized:
            raise ScryfallValidationException(
                "'bulk_type' cannot be empty.",
                params={"bulk_type": bulk_type},
            )
        if len(normalized) > _MAX_BULK_TYPE_LEN:
            raise ScryfallValidationException(
                "'bulk_type' is too long.",
                params={"bulk_type": bulk_type},
            )
        if not _BULK_TYPE_SLUG_PATTERN.match(normalized):
            raise ScryfallValidationException(
                "'bulk_type' has an invalid format (expected kebab-case segments).",
                params={"bulk_type": bulk_type},
            )
        return normalized

    def download_bulk_dataset(
        self,
        *,
        bulk_data: BulkData,
        destination_path: Path | str,
        overwrite: bool = False,
        chunk_size: int = 1024 * 64,
    ) -> BulkDownloadResult:
        """Telecharge le fichier indique par ``bulk_data.download_uri`` vers le disque local.

        Requiert un :class:`BulkDatasetDownloader` injecte au constructeur (ou via la facade
        :class:`~baobab_scryfall_api_caller.client.scryfall_api_caller.ScryfallApiCaller`).

        :param bulk_data: Metadonnees (notamment ``download_uri``) obtenues via l'API Scryfall.
        :param destination_path: Chemin **fichier** cible (repertoire parent cree si besoin).
        :param overwrite: Si ``False``, refuser d'ecraser un fichier deja present.
        :param chunk_size: Taille de chunk pour le streaming (defaut 64 Kio).
        """
        if self._bulk_dataset_downloader is None:
            raise ScryfallValidationException(
                "Bulk dataset download requires a BulkDatasetDownloader. Pass "
                "'bulk_dataset_downloader' when constructing BulkDataService or ScryfallApiCaller.",
                params={"bulk_dataset_downloader": None},
            )
        return self._bulk_dataset_downloader.download(
            bulk_data=bulk_data,
            destination_path=destination_path,
            overwrite=overwrite,
            chunk_size=chunk_size,
        )

    def download_bulk_dataset_by_type(
        self,
        bulk_type: str,
        destination_path: Path | str,
        *,
        overwrite: bool = False,
        chunk_size: int = 1024 * 64,
    ) -> BulkDownloadResult:
        """Recupere les metadonnees par type puis telecharge le fichier associe."""
        meta = self.get_by_type(bulk_type)
        return self.download_bulk_dataset(
            bulk_data=meta,
            destination_path=destination_path,
            overwrite=overwrite,
            chunk_size=chunk_size,
        )

    def download_bulk_dataset_by_id(
        self,
        bulk_data_id: str,
        destination_path: Path | str,
        *,
        overwrite: bool = False,
        chunk_size: int = 1024 * 64,
    ) -> BulkDownloadResult:
        """Recupere les metadonnees par UUID puis telecharge le fichier associe."""
        meta = self.get_by_id(bulk_data_id)
        return self.download_bulk_dataset(
            bulk_data=meta,
            destination_path=destination_path,
            overwrite=overwrite,
            chunk_size=chunk_size,
        )
