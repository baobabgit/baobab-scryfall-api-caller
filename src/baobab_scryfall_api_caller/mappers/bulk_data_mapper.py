"""Mapper de payload bulk_data Scryfall vers objets metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import (
    ScryfallBulkDataException,
    ScryfallResponseFormatException,
)
from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData


class BulkDataMapper:
    """Mappe une reponse ``bulk_data`` brute vers `BulkData`."""

    def map_bulk_data(self, raw_bulk: Any) -> BulkData:
        """Transforme un payload Scryfall en modele `BulkData`."""
        if not isinstance(raw_bulk, dict):
            raise ScryfallResponseFormatException(
                "Bulk data payload must be a dictionary.",
                response_detail=raw_bulk,
            )

        if raw_bulk.get("object") != "bulk_data":
            raise ScryfallResponseFormatException(
                "Bulk data payload has an invalid 'object' field.",
                response_detail=raw_bulk,
            )

        bulk_id = raw_bulk.get("id")
        uri = raw_bulk.get("uri")
        bulk_type = raw_bulk.get("type")
        name = raw_bulk.get("name")
        description = raw_bulk.get("description")
        download_uri = raw_bulk.get("download_uri")
        updated_at = raw_bulk.get("updated_at")
        size_raw = raw_bulk.get("size")
        content_type = raw_bulk.get("content_type")
        content_encoding = raw_bulk.get("content_encoding")

        if not isinstance(bulk_id, str) or not bulk_id:
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'id'.",
                response_detail=raw_bulk,
            )
        if not isinstance(uri, str) or not uri:
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'uri'.",
                response_detail=raw_bulk,
            )
        if not isinstance(bulk_type, str) or not bulk_type:
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'type'.",
                response_detail=raw_bulk,
            )
        if not isinstance(name, str) or not name:
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'name'.",
                response_detail=raw_bulk,
            )
        if not isinstance(description, str):
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'description'.",
                response_detail=raw_bulk,
            )
        if not isinstance(download_uri, str) or not download_uri.strip():
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'download_uri'.",
                response_detail=raw_bulk,
            )
        if not isinstance(updated_at, str) or not updated_at:
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'updated_at'.",
                response_detail=raw_bulk,
            )
        if not isinstance(size_raw, int) or size_raw < 0:
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'size'.",
                response_detail=raw_bulk,
            )
        if not isinstance(content_type, str) or not content_type:
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'content_type'.",
                response_detail=raw_bulk,
            )
        if not isinstance(content_encoding, str) or not content_encoding:
            raise ScryfallResponseFormatException(
                "Bulk data payload is missing a valid 'content_encoding'.",
                response_detail=raw_bulk,
            )

        self._assert_coherent_download_metadata(
            download_uri=download_uri,
            size=size_raw,
            response_detail=raw_bulk,
        )

        return BulkData(
            id=bulk_id,
            uri=uri,
            type=bulk_type,
            name=name,
            description=description,
            download_uri=download_uri,
            updated_at=updated_at,
            size=size_raw,
            content_type=content_type,
            content_encoding=content_encoding,
        )

    @staticmethod
    def _assert_coherent_download_metadata(
        *,
        download_uri: str,
        size: int,
        response_detail: dict[str, Any],
    ) -> None:
        """Verifie la coherence minimale des metadonnees de telechargement."""
        if not download_uri.startswith(("http://", "https://")):
            raise ScryfallBulkDataException(
                "Bulk data download_uri must be an absolute HTTP(S) URL.",
                response_detail=response_detail,
            )
        if size == 0:
            raise ScryfallBulkDataException(
                "Bulk data size must be strictly positive for a published dataset.",
                response_detail=response_detail,
            )
