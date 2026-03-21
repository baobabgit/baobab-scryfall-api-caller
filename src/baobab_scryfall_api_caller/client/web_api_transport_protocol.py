"""Protocole structurel pour le transport injecte (baobab-web-api-caller ou doubles)."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class WebApiTransportProtocol(Protocol):
    """Contrat minimal pour les implementations passees a `ScryfallApiCaller`.

    La bibliotheque `baobab-web-api-caller` fournit notamment
    :class:`baobab_web_api_caller.service.baobab_service_caller.BaobabServiceCaller`,
    qui expose des methodes ``get`` / ``post`` compatibles avec les essais effectues
    par `ScryfallHttpClient`.

    Le protocole reste volontairement structurel (``Any`` en retour) pour ne pas
    sur-contraindre les mocks.
    """

    def get(self, *args: Any, **kwargs: Any) -> Any:
        """Execute un GET vers l'API distante."""

    def post(self, *args: Any, **kwargs: Any) -> Any:
        """Execute un POST vers l'API distante."""
