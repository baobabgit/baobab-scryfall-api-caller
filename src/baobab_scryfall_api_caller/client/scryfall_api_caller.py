"""Facade principale : exposition des services domaine sans logique metier."""

from __future__ import annotations

from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.services.bulk_data.bulk_data_service import BulkDataService
from baobab_scryfall_api_caller.services.cards.cards_service import CardsService
from baobab_scryfall_api_caller.services.catalogs.catalogs_service import CatalogsService
from baobab_scryfall_api_caller.services.rulings.rulings_service import RulingsService
from baobab_scryfall_api_caller.services.sets.sets_service import SetsService


class ScryfallApiCaller:
    """Point d'entree unique pour acceder aux services Scryfall V1.

    Cette classe ne concentre pas la logique metier : elle regroupe les services
    (`cards`, `sets`, `rulings`, `catalogs`, `bulk_data`) initialises avec le
    meme transport HTTP (`baobab-web-api-caller`).

    Le domaine **Cards** (attribut ``cards``, type `CardsService`) expose l'integralite
    du perimetre V1 documente (acces unitaires, named, search, autocomplete, random,
    collection).

    Chaque service est injectable pour les tests ou les extensions ; par defaut,
    les instances sont construites avec le meme ``web_api_caller``.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        cards_service: CardsService | None = None,
        sets_service: SetsService | None = None,
        rulings_service: RulingsService | None = None,
        catalogs_service: CatalogsService | None = None,
        bulk_data_service: BulkDataService | None = None,
    ) -> None:
        """Initialise la facade avec le transport et les services optionnels.

        :param web_api_caller: implementation ``baobab-web-api-caller`` a utiliser
            pour tous les appels HTTP (ex. `WebApiCaller` configure pour Scryfall).
        :param cards_service: service Cards ; sinon construit avec ``web_api_caller``.
        :param sets_service: service Sets ; sinon construit avec ``web_api_caller``.
        :param rulings_service: service Rulings ; sinon construit avec ``web_api_caller``.
        :param catalogs_service: service Catalogs ; sinon construit avec ``web_api_caller``.
        :param bulk_data_service: service Bulk Data ; sinon construit avec ``web_api_caller``.

        :raises ScryfallValidationException: si ``web_api_caller`` est absent.
        """
        if web_api_caller is None:
            raise ScryfallValidationException(
                "'web_api_caller' is required.",
                params={"web_api_caller": web_api_caller},
            )
        self._web_api_caller: WebApiTransportProtocol = web_api_caller
        self.cards = cards_service or CardsService(web_api_caller=web_api_caller)
        self.sets = sets_service or SetsService(web_api_caller=web_api_caller)
        self.rulings = rulings_service or RulingsService(web_api_caller=web_api_caller)
        self.catalogs = catalogs_service or CatalogsService(web_api_caller=web_api_caller)
        self.bulk_data = bulk_data_service or BulkDataService(web_api_caller=web_api_caller)

    @property
    def web_api_caller(self) -> WebApiTransportProtocol:
        """Transport HTTP injecte (meme instance que celle passee au constructeur)."""
        return self._web_api_caller
