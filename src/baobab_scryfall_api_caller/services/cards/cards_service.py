"""Service metier Cards (premier perimetre)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.mappers.autocomplete_mapper import AutocompleteMapper
from baobab_scryfall_api_caller.mappers.card_collection_mapper import CardCollectionMapper
from baobab_scryfall_api_caller.mappers.card_mapper import CardMapper
from baobab_scryfall_api_caller.models.cards.autocomplete_result import AutocompleteResult
from baobab_scryfall_api_caller.models.cards.card import Card
from baobab_scryfall_api_caller.models.cards.card_collection_constants import (
    MAX_CARD_COLLECTION_IDENTIFIERS,
)
from baobab_scryfall_api_caller.models.cards.card_collection_identifier import (
    CardCollectionIdentifier,
)
from baobab_scryfall_api_caller.models.cards.card_collection_result import CardCollectionResult
from baobab_scryfall_api_caller.models.common.list_response import ListResponse
from baobab_scryfall_api_caller.pagination.scryfall_list_response_parser import (
    ScryfallListResponseParser,
)
from baobab_scryfall_api_caller.services.cards.cards_api_client import CardsApiClient
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)


class CardsService:
    """Service metier du domaine **Cards** Scryfall (conformite V1).

    Couvre les acces unitaires, la recherche DSL, l'autocompletion, le tirage aleatoire
    et la resolution en lot (`POST /cards/collection`). Les erreurs de validation locale
    levent `ScryfallValidationException` ; les erreurs transport / HTTP / format de
    reponse sont traduites par `ScryfallHttpClient` et les mappers.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        api_client: CardsApiClient | None = None,
        card_mapper: CardMapper | None = None,
        list_parser: ScryfallListResponseParser | None = None,
        autocomplete_mapper: AutocompleteMapper | None = None,
        collection_mapper: CardCollectionMapper | None = None,
    ) -> None:
        """Initialise le service Cards et les mappers / clients injectables."""
        self.api_client = api_client or CardsApiClient(web_api_caller=web_api_caller)
        self.card_mapper = card_mapper or CardMapper()
        self.list_parser = list_parser or ScryfallListResponseParser()
        self.autocomplete_mapper = autocomplete_mapper or AutocompleteMapper()
        self.collection_mapper = collection_mapper or CardCollectionMapper(
            card_mapper=self.card_mapper,
        )

    def get_by_id(self, card_id: str) -> Card:
        """Recupere une carte par identifiant Scryfall (`GET /cards/{id}`).

        :return: Carte mappee.
        """
        normalized_card_id = ScryfallRequestValidators.require_non_empty_text(
            value=card_id,
            field_name="card_id",
        )
        payload = self.api_client.get(route=f"/cards/{normalized_card_id}")
        return self.card_mapper.map_card(payload)

    def get_by_mtgo_id(self, mtgo_id: int) -> Card:
        """Recupere une carte par identifiant MTGO (`GET /cards/mtgo/{id}`)."""
        normalized_mtgo_id = ScryfallRequestValidators.require_strict_positive_int(
            value=mtgo_id,
            field_name="mtgo_id",
        )
        payload = self.api_client.get(route=f"/cards/mtgo/{normalized_mtgo_id}")
        return self.card_mapper.map_card(payload)

    def get_by_cardmarket_id(self, cardmarket_id: int) -> Card:
        """Recupere une carte par identifiant Cardmarket (`GET /cards/cardmarket/{id}`)."""
        normalized_cardmarket_id = ScryfallRequestValidators.require_strict_positive_int(
            value=cardmarket_id,
            field_name="cardmarket_id",
        )
        payload = self.api_client.get(route=f"/cards/cardmarket/{normalized_cardmarket_id}")
        return self.card_mapper.map_card(payload)

    def get_by_set_and_number(self, set_code: str, collector_number: str) -> Card:
        """Recupere une carte par code d'extension + numero de collection.

        (`GET /cards/{set}/{collector_number}` — code d'extension normalise en minuscules.)
        """
        normalized_set_code = ScryfallRequestValidators.require_non_empty_text(
            value=set_code,
            field_name="set_code",
        )
        normalized_collector_number = ScryfallRequestValidators.require_non_empty_text(
            value=collector_number,
            field_name="collector_number",
        )
        payload = self.api_client.get(
            route=f"/cards/{normalized_set_code.lower()}/{normalized_collector_number}",
        )
        return self.card_mapper.map_card(payload)

    def get_named(self, *, exact: str | None = None, fuzzy: str | None = None) -> Card:
        """Recupere une carte via endpoint named (exact ou fuzzy)."""
        if exact and fuzzy:
            raise ScryfallValidationException(
                "Only one of 'exact' or 'fuzzy' can be provided for named lookup.",
                params={"exact": exact, "fuzzy": fuzzy},
            )
        if not exact and not fuzzy:
            raise ScryfallValidationException(
                "One of 'exact' or 'fuzzy' must be provided for named lookup.",
                params={"exact": exact, "fuzzy": fuzzy},
            )

        params: dict[str, str]
        if exact is not None:
            normalized_exact = ScryfallRequestValidators.require_non_empty_text(
                value=exact,
                field_name="exact",
            )
            params = {"exact": normalized_exact}
        else:
            assert fuzzy is not None
            normalized_fuzzy = ScryfallRequestValidators.require_non_empty_text(
                value=fuzzy,
                field_name="fuzzy",
            )
            params = {"fuzzy": normalized_fuzzy}

        payload = self.api_client.get(route="/cards/named", params=params)
        return self.card_mapper.map_card(payload)

    def search(self, *, q: str, page: int | None = None) -> ListResponse[Card]:
        """Recherche de cartes via le DSL Scryfall (`GET /cards/search`, liste paginee).

        Le parametre ``q`` est transmis tel quel a l'API (sans reecriture du DSL),
        apres validation de type et de non-vide (strip pour le test de vide uniquement).
        """
        validated_q = ScryfallRequestValidators.require_scryfall_query_string(
            value=q,
            field_name="q",
        )
        params: dict[str, Any] = {"q": validated_q}
        page_params = ScryfallRequestValidators.optional_page_params(page=page)
        if page_params is not None:
            params.update(page_params)
        payload = self.api_client.get(route="/cards/search", params=params)
        return self.list_parser.parse(
            raw_response=payload,
            item_mapper=self.card_mapper.map_card,
        )

    def autocomplete(self, *, q: str) -> AutocompleteResult:
        """Suggestions de noms (`GET /cards/autocomplete`)."""
        validated_q = ScryfallRequestValidators.require_scryfall_query_string(
            value=q,
            field_name="q",
        )
        payload = self.api_client.get(
            route="/cards/autocomplete",
            params={"q": validated_q},
        )
        return self.autocomplete_mapper.map_autocomplete(payload)

    def random(self, *, q: str | None = None) -> Card:
        """Recupere une carte aleatoire, optionnellement filtree par DSL ``q``."""
        params: dict[str, str] | None = None
        if q is not None:
            validated_q = ScryfallRequestValidators.require_scryfall_query_string(
                value=q,
                field_name="q",
            )
            params = {"q": validated_q}
        payload = self.api_client.get(route="/cards/random", params=params)
        return self.card_mapper.map_card(payload)

    def get_collection(
        self,
        *,
        identifiers: Sequence[CardCollectionIdentifier],
    ) -> CardCollectionResult:
        """Resolution en lot (`POST /cards/collection`, max 75 identifiants).

        Les cartes trouvees sont mappees en `Card` ; les identifiants non resolus
        sont exposes dans ``not_found`` (meme structure que cote Scryfall).
        """
        self._validate_collection_identifiers(identifiers=identifiers)
        request_body = {
            "identifiers": [item.to_api_dict() for item in identifiers],
        }
        payload = self.api_client.post(route="/cards/collection", payload=request_body)
        return self.collection_mapper.map_collection_response(payload)

    @staticmethod
    def _validate_collection_identifiers(
        *,
        identifiers: Sequence[CardCollectionIdentifier],
    ) -> None:
        """Valide le type, la taille et les elements de la sequence d'identifiants."""
        if isinstance(identifiers, (str, bytes)):
            raise ScryfallValidationException(
                "'identifiers' must be a sequence of CardCollectionIdentifier, not a string.",
                params={"identifiers": identifiers},
            )
        if not isinstance(identifiers, Sequence):
            raise ScryfallValidationException(
                "'identifiers' must be a sequence of CardCollectionIdentifier.",
                params={"identifiers": identifiers},
            )
        count = len(identifiers)
        if count == 0:
            raise ScryfallValidationException(
                "'identifiers' cannot be empty.",
                params={"identifiers": identifiers},
            )
        if count > MAX_CARD_COLLECTION_IDENTIFIERS:
            raise ScryfallValidationException(
                f"A maximum of {MAX_CARD_COLLECTION_IDENTIFIERS} identifiers is allowed "
                "per collection request.",
                params={"count": count, "max": MAX_CARD_COLLECTION_IDENTIFIERS},
            )
        for index, item in enumerate(identifiers):
            if not isinstance(item, CardCollectionIdentifier):
                raise ScryfallValidationException(
                    f"Item at index {index} must be a CardCollectionIdentifier.",
                    params={"index": index, "item": item},
                )
