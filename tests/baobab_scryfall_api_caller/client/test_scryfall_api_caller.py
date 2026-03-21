"""Tests de la facade publique ScryfallApiCaller."""

from __future__ import annotations

import baobab_scryfall_api_caller
from baobab_scryfall_api_caller.client.scryfall_api_caller import ScryfallApiCaller
from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.services.bulk_data.bulk_data_service import BulkDataService
from baobab_scryfall_api_caller.services.cards.cards_service import CardsService
from baobab_scryfall_api_caller.services.catalogs.catalogs_service import CatalogsService
from baobab_scryfall_api_caller.services.rulings.rulings_service import RulingsService
from baobab_scryfall_api_caller.services.sets.sets_service import SetsService


class TestScryfallApiCaller:
    """Validation de l'initialisation et de l'exposition des services."""

    def test_init_requires_web_api_caller(self) -> None:
        """Sans transport, la facade doit lever une erreur de validation."""
        try:
            ScryfallApiCaller(web_api_caller=None)  # type: ignore[arg-type]
        except ScryfallValidationException as exc:
            assert "web_api_caller" in str(exc).lower() or exc.params.get("web_api_caller") is None
        else:
            assert False, "Expected ScryfallValidationException"

    def test_default_services_types(self) -> None:
        """Les services par defaut sont les classes domaine attendues."""
        transport = object()
        api = ScryfallApiCaller(web_api_caller=transport)
        assert isinstance(api.cards, CardsService)
        assert isinstance(api.sets, SetsService)
        assert isinstance(api.rulings, RulingsService)
        assert isinstance(api.catalogs, CatalogsService)
        assert isinstance(api.bulk_data, BulkDataService)

    def test_default_services_share_transport(self) -> None:
        """Chaque client domaine doit reutiliser le meme transport injecte."""
        transport = object()
        api = ScryfallApiCaller(web_api_caller=transport)
        assert api.cards.api_client._http.web_api_caller is transport
        assert api.sets.api_client._http.web_api_caller is transport
        assert api.rulings.api_client._http.web_api_caller is transport
        assert api.catalogs.api_client._http.web_api_caller is transport
        assert api.bulk_data.api_client._http.web_api_caller is transport

    def test_web_api_caller_property(self) -> None:
        """La propriete expose le transport sans copie."""
        transport = object()
        api = ScryfallApiCaller(web_api_caller=transport)
        assert api.web_api_caller is transport

    def test_injected_cards_service_preserved(self) -> None:
        """Un service Cards injecte doit etre conserve tel quel."""
        transport = object()
        custom = CardsService(web_api_caller=transport)
        api = ScryfallApiCaller(web_api_caller=transport, cards_service=custom)
        assert api.cards is custom

    def test_package_root_exports_scryfall_api_caller(self) -> None:
        """Le package racine reexporte ScryfallApiCaller."""
        assert hasattr(baobab_scryfall_api_caller, "ScryfallApiCaller")
        assert "ScryfallApiCaller" in baobab_scryfall_api_caller.__all__

    def test_package_root_exports_web_api_transport_protocol(self) -> None:
        """Le protocole de transport est reexporte pour le typage des integrations."""
        assert hasattr(baobab_scryfall_api_caller, "WebApiTransportProtocol")
        assert "WebApiTransportProtocol" in baobab_scryfall_api_caller.__all__

    def test_import_from_client_subpackage_matches_root(self) -> None:
        """Les imports racine et sous-package client designent la meme classe."""
        from baobab_scryfall_api_caller.client import ScryfallApiCaller as FromClient

        assert FromClient is ScryfallApiCaller
