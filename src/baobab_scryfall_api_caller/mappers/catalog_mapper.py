"""Mapper de payload catalogue Scryfall vers objets metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.models.catalogs.catalog import Catalog


class CatalogMapper:
    """Mappe une reponse catalogue brute vers `Catalog`."""

    def map_catalog(self, raw_catalog: Any, *, catalog_key: str) -> Catalog:
        """Transforme un payload Scryfall ``catalog`` en modele `Catalog`.

        :param raw_catalog: Corps JSON brut de la reponse.
        :param catalog_key: Cle normalisee utilisee pour la requete (segment d'URL).
        :return: Instance `Catalog` typee.
        """
        if not isinstance(raw_catalog, dict):
            raise ScryfallResponseFormatException(
                "Catalog payload must be a dictionary.",
                response_detail=raw_catalog,
            )

        if raw_catalog.get("object") != "catalog":
            raise ScryfallResponseFormatException(
                "Catalog payload has an invalid 'object' field.",
                response_detail=raw_catalog,
            )

        uri = raw_catalog.get("uri")
        if not isinstance(uri, str) or not uri:
            raise ScryfallResponseFormatException(
                "Catalog payload is missing a valid 'uri'.",
                response_detail=raw_catalog,
            )

        total_raw = raw_catalog.get("total_values")
        if not isinstance(total_raw, int) or total_raw < 0:
            raise ScryfallResponseFormatException(
                "Catalog payload is missing a valid 'total_values'.",
                response_detail=raw_catalog,
            )

        raw_data = raw_catalog.get("data")
        if not isinstance(raw_data, list):
            raise ScryfallResponseFormatException(
                "Catalog payload has an invalid 'data' field.",
                response_detail=raw_catalog,
            )

        values: list[str] = []
        for index, item in enumerate(raw_data):
            if not isinstance(item, str):
                raise ScryfallResponseFormatException(
                    f"Catalog payload has a non-string value at index {index}.",
                    response_detail=raw_catalog,
                )
            values.append(item)

        return Catalog(
            catalog_key=catalog_key,
            uri=uri,
            total_values=total_raw,
            values=tuple(values),
        )
