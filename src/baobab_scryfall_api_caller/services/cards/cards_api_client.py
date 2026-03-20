"""Client technique pour appeler les endpoints Cards via baobab-web-api-caller."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.error_translation_context import ErrorTranslationContext
from baobab_scryfall_api_caller.mappers.scryfall_error_translator import ScryfallErrorTranslator


class CardsApiClient:
    """Encapsule les appels HTTP du domaine cards."""

    def __init__(
        self,
        *,
        web_api_caller: Any,
        error_translator: ScryfallErrorTranslator | None = None,
    ) -> None:
        """Initialise le client technique Cards."""
        self.web_api_caller = web_api_caller
        self.error_translator = error_translator or ScryfallErrorTranslator()

    def get(self, *, route: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute un GET et retourne un payload dictionnaire."""
        try:
            raw_response = self._perform_get(route=route, params=params)
        except Exception as error:  # pylint: disable=broad-exception-caught
            raise self.error_translator.translate(
                error=error,
                context=ErrorTranslationContext(
                    url=route,
                    params=params,
                ),
            ) from error

        payload = self._extract_payload(raw_response)
        status_code = self._extract_status_code(raw_response, payload)
        if status_code >= 400 or payload.get("object") == "error":
            translated = self.error_translator.translate(
                context=ErrorTranslationContext(
                    message=self._extract_error_message(payload, status_code),
                    http_status=(
                        status_code if status_code >= 400 else self._extract_error_status(payload)
                    ),
                    url=route,
                    params=params,
                    response_detail=payload,
                )
            )
            raise translated

        return payload

    def _perform_get(self, *, route: str, params: dict[str, Any] | None) -> Any:
        headers = {"Accept": "application/json"}
        candidate_payloads = [
            {"route": route, "params": params, "headers": headers},
            {"path": route, "params": params, "headers": headers},
            {"url": route, "params": params, "headers": headers},
        ]
        for payload in candidate_payloads:
            try:
                return self.web_api_caller.get(**payload)
            except TypeError:
                continue
        return self.web_api_caller.get(route, params=params, headers=headers)

    @staticmethod
    def _extract_payload(raw_response: Any) -> dict[str, Any]:
        if isinstance(raw_response, dict):
            return raw_response

        if hasattr(raw_response, "json") and callable(raw_response.json):
            payload = raw_response.json()
            if isinstance(payload, dict):
                return payload

        raise ScryfallResponseFormatException(
            "Cards API client received an invalid response format.",
            response_detail=raw_response,
        )

    @staticmethod
    def _extract_status_code(raw_response: Any, payload: dict[str, Any]) -> int:
        for key in ("status_code", "status"):
            value = getattr(raw_response, key, None)
            if isinstance(value, int):
                return value
        payload_status = payload.get("status")
        if isinstance(payload_status, int):
            return payload_status
        return 200

    @staticmethod
    def _extract_error_status(payload: dict[str, Any]) -> int | None:
        status = payload.get("status")
        if isinstance(status, int):
            return status
        return None

    @staticmethod
    def _extract_error_message(payload: dict[str, Any], status_code: int) -> str:
        details = payload.get("details")
        if isinstance(details, str) and details:
            return details
        if status_code >= 400:
            return f"Scryfall cards request failed with HTTP status {status_code}."
        return "Scryfall cards request failed."
