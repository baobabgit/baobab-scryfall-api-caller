"""Couche HTTP commune pour les appels Scryfall via baobab-web-api-caller."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.client.baobab_query_params_normalizer import (
    BaobabQueryParamsNormalizer,
)
from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol
from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.error_translation_context import ErrorTranslationContext
from baobab_scryfall_api_caller.mappers.scryfall_error_translator import ScryfallErrorTranslator


class ScryfallHttpClient:
    """Execute GET/POST JSON et normalise les erreurs via `ScryfallErrorTranslator`.

    Le transport injecte est typiquement une instance de
    :class:`baobab_web_api_caller.service.baobab_service_caller.BaobabServiceCaller`
    (raccourcis ``get`` / ``post`` avec ``path``, ``query_params``, ``json_body``)
    ou tout double de test exposant les memes conventions.

    Les signatures historiques ``route`` / ``params`` / ``json`` restent essayees en
    premier pour la compatibilite avec les mocks existants.
    """

    def __init__(
        self,
        *,
        web_api_caller: WebApiTransportProtocol,
        error_translator: ScryfallErrorTranslator | None = None,
    ) -> None:
        """Initialise le client HTTP partage.

        :param web_api_caller: couche de transport ``baobab-web-api-caller`` (ex.
            `BaobabServiceCaller` compose avec `HttpTransportCaller`).
        """
        self.web_api_caller: WebApiTransportProtocol = web_api_caller
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

    def post(
        self,
        *,
        route: str,
        payload: dict[str, Any],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute un POST JSON et retourne un payload dictionnaire."""
        try:
            raw_response = self._perform_post(route=route, payload=payload, params=params)
        except Exception as error:  # pylint: disable=broad-exception-caught
            raise self.error_translator.translate(
                error=error,
                context=ErrorTranslationContext(
                    url=route,
                    params=params,
                    payload=payload,
                ),
            ) from error

        normalized_payload = self._extract_payload(raw_response)
        status_code = self._extract_status_code(raw_response, normalized_payload)
        if status_code >= 400 or normalized_payload.get("object") == "error":
            translated = self.error_translator.translate(
                context=ErrorTranslationContext(
                    message=self._extract_error_message(normalized_payload, status_code),
                    http_status=(
                        status_code
                        if status_code >= 400
                        else self._extract_error_status(normalized_payload)
                    ),
                    url=route,
                    params=params,
                    payload=payload,
                    response_detail=normalized_payload,
                )
            )
            raise translated

        return normalized_payload

    def _perform_get(self, *, route: str, params: dict[str, Any] | None) -> Any:
        headers = {"Accept": "application/json"}
        baobab_query = BaobabQueryParamsNormalizer.normalize(params)
        query_params = {} if baobab_query is None else baobab_query
        candidate_payloads: list[dict[str, Any]] = [
            {"route": route, "params": params, "headers": headers},
            {"path": route, "params": params, "headers": headers},
            {"url": route, "params": params, "headers": headers},
            {"path": route, "query_params": query_params, "headers": headers},
        ]
        for payload in candidate_payloads:
            try:
                return self.web_api_caller.get(**payload)
            except TypeError:
                continue
        return self.web_api_caller.get(route, params=params, headers=headers)

    def _perform_post(
        self,
        *,
        route: str,
        payload: dict[str, Any],
        params: dict[str, Any] | None,
    ) -> Any:
        headers = {"Accept": "application/json"}
        baobab_query = BaobabQueryParamsNormalizer.normalize(params)
        query_params = {} if baobab_query is None else baobab_query
        candidate_payloads: list[dict[str, Any]] = [
            {"route": route, "params": params, "json": payload, "headers": headers},
            {"route": route, "params": params, "payload": payload, "headers": headers},
            {"path": route, "params": params, "json": payload, "headers": headers},
            {"url": route, "params": params, "json": payload, "headers": headers},
            {
                "path": route,
                "query_params": query_params,
                "json_body": payload,
                "headers": headers,
            },
        ]
        for request_payload in candidate_payloads:
            try:
                return self.web_api_caller.post(**request_payload)
            except TypeError:
                continue
        return self.web_api_caller.post(route, params=params, json=payload, headers=headers)

    @staticmethod
    def _extract_payload(raw_response: Any) -> dict[str, Any]:
        if isinstance(raw_response, dict):
            return raw_response

        json_data = getattr(raw_response, "json_data", None)
        if isinstance(json_data, dict):
            return json_data

        if hasattr(raw_response, "json") and callable(raw_response.json):
            payload = raw_response.json()
            if isinstance(payload, dict):
                return payload

        raise ScryfallResponseFormatException(
            "Scryfall API client received an invalid response format.",
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
            return f"Scryfall request failed with HTTP status {status_code}."
        return "Scryfall request failed."
