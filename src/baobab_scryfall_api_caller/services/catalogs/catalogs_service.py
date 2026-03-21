"""Service metier Catalogs (valeurs de reference Scryfall)."""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

from baobab_scryfall_api_caller.cache.json_response_cache import JsonResponseCache
from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.mappers.catalog_mapper import CatalogMapper
from baobab_scryfall_api_caller.models.catalogs.catalog import Catalog
from baobab_scryfall_api_caller.services.catalogs.catalogs_api_client import CatalogsApiClient

_CATALOG_KEY_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_MAX_CATALOG_KEY_LEN = 80


class CatalogsService:
    """Expose l'acces aux catalogues Scryfall (generique + helpers V1).

    Les helpers deleguent a :meth:`get_catalog` pour conserver une seule voie
    de construction d'URL, de validation transport et de mapping.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        api_client: CatalogsApiClient | None = None,
        catalog_mapper: CatalogMapper | None = None,
        response_cache: JsonResponseCache | None = None,
        cacheable_get_predicate: Callable[[str, dict[str, Any] | None], bool] | None = None,
    ) -> None:
        """Initialise le service Catalogs avec ses dependances."""
        self.api_client = api_client or CatalogsApiClient(
            web_api_caller=web_api_caller,
            response_cache=response_cache,
            cacheable_get_predicate=cacheable_get_predicate,
        )
        self.catalog_mapper = catalog_mapper or CatalogMapper()

    def get_catalog(self, catalog_key: str) -> Catalog:
        """Recupere un catalogue par sa cle d'URL (ex. ``card-names``).

        :param catalog_key: Segment du chemin ``/catalog/{catalog_key}``, normalise
            en minuscules ; doit respecter le motif kebab-case Scryfall.
        :return: Catalogue type `Catalog`.
        """
        normalized = self._require_catalog_key(catalog_key=catalog_key)
        payload = self.api_client.get(route=f"/catalog/{normalized}")
        return self.catalog_mapper.map_catalog(payload, catalog_key=normalized)

    def get_card_names(self) -> Catalog:
        """Raccourci vers le catalogue des noms de cartes."""
        return self.get_catalog("card-names")

    def get_creature_types(self) -> Catalog:
        """Raccourci vers le catalogue des types de creature."""
        return self.get_catalog("creature-types")

    def get_land_types(self) -> Catalog:
        """Raccourci vers le catalogue des types de terrain."""
        return self.get_catalog("land-types")

    def get_card_types(self) -> Catalog:
        """Raccourci vers le catalogue des types de carte."""
        return self.get_catalog("card-types")

    def get_artist_names(self) -> Catalog:
        """Raccourci vers le catalogue des noms d'artistes."""
        return self.get_catalog("artist-names")

    @staticmethod
    def _require_catalog_key(*, catalog_key: str) -> str:
        if not isinstance(catalog_key, str):
            raise ScryfallValidationException(
                "'catalog_key' must be a string.",
                params={"catalog_key": catalog_key},
            )
        normalized = catalog_key.strip().lower()
        if not normalized:
            raise ScryfallValidationException(
                "'catalog_key' cannot be empty.",
                params={"catalog_key": catalog_key},
            )
        if len(normalized) > _MAX_CATALOG_KEY_LEN:
            raise ScryfallValidationException(
                "'catalog_key' is too long.",
                params={"catalog_key": catalog_key},
            )
        if not _CATALOG_KEY_PATTERN.match(normalized):
            raise ScryfallValidationException(
                "'catalog_key' has an invalid format (expected kebab-case segments).",
                params={"catalog_key": catalog_key},
            )
        return normalized
