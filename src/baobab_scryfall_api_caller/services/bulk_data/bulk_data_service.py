"""Service metier Bulk Data (metadonnees des exports Scryfall)."""

from __future__ import annotations

import re

from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.mappers.bulk_data_mapper import BulkDataMapper
from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData
from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.pagination.scryfall_list_response_parser import (
    ScryfallListResponseParser,
)
from baobab_scryfall_api_caller.services.bulk_data.bulk_data_api_client import BulkDataApiClient
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)

_BULK_TYPE_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_MAX_BULK_TYPE_LEN = 80


class BulkDataService:
    """Expose les operations Bulk Data V1 (liste et metadonnees, sans telechargement).

    Une extension future pourra ajouter le telechargement en s'appuyant sur les
    memes dependances injectees sans modifier la signature du constructeur.
    """

    def __init__(
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        api_client: BulkDataApiClient | None = None,
        bulk_data_mapper: BulkDataMapper | None = None,
        list_parser: ScryfallListResponseParser | None = None,
    ) -> None:
        """Initialise le service Bulk Data avec ses dependances."""
        self.api_client = api_client or BulkDataApiClient(web_api_caller=web_api_caller)
        self.bulk_data_mapper = bulk_data_mapper or BulkDataMapper()
        self.list_parser = list_parser or ScryfallListResponseParser()

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
