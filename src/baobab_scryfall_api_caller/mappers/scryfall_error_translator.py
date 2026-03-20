"""Traduction des erreurs techniques vers les exceptions metier du projet."""

from __future__ import annotations

from baobab_scryfall_api_caller.exceptions import (
    BaobabScryfallApiCallerException,
    ScryfallBulkDataException,
    ScryfallNotFoundException,
    ScryfallPaginationException,
    ScryfallRateLimitException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.mappers.error_translation_context import (
    ErrorTranslationContext,
)


class ScryfallErrorTranslator:
    """Traduit des erreurs transport/validation/format vers des erreurs metier.

    Le composant est volontairement decouple de toute implementation concrete
    de `baobab-web-api-caller`. Il consomme uniquement :
    - des exceptions Python standard ou custom ;
    - des metadonnees optionnelles (`http_status`, `url`, etc.).
    """

    def translate(
        self,
        *,
        error: Exception | None = None,
        context: ErrorTranslationContext | None = None,
    ) -> BaobabScryfallApiCallerException:
        """Traduit un contexte d'erreur brut en exception metier.

        :param error: Erreur d'origine.
        :param context: Contexte optionnel de traduction.
        :return: Exception metier typique a lever.
        """
        resolved_context = context or ErrorTranslationContext()
        resolved_status = (
            resolved_context.http_status
            if resolved_context.http_status is not None
            else self._extract_status(error)
        )
        resolved_message = self._resolve_message(
            message=resolved_context.message,
            error=error,
            status=resolved_status,
        )
        exception_type = self._resolve_exception_type(
            category=resolved_context.category,
            status=resolved_status,
            error=error,
        )

        return exception_type(
            resolved_message,
            http_status=resolved_status,
            url=resolved_context.url,
            params=resolved_context.params,
            payload=resolved_context.payload,
            response_detail=resolved_context.response_detail,
            cause=error,
        )

    def _resolve_exception_type(
        self,
        *,
        category: str | None,
        status: int | None,
        error: Exception | None,
    ) -> type[BaobabScryfallApiCallerException]:
        forced_types: dict[str, type[BaobabScryfallApiCallerException]] = {
            "validation": ScryfallValidationException,
            "pagination": ScryfallPaginationException,
            "bulk_data": ScryfallBulkDataException,
            "response_format": ScryfallResponseFormatException,
            "request": ScryfallRequestException,
        }
        if category in forced_types:
            return forced_types[category]
        if status == 404:
            return ScryfallNotFoundException
        if status == 429:
            return ScryfallRateLimitException
        if self._is_response_format_error(error):
            return ScryfallResponseFormatException
        if self._is_validation_error(error):
            return ScryfallValidationException
        return ScryfallRequestException

    @staticmethod
    def _extract_status(error: Exception | None) -> int | None:
        if error is None:
            return None

        for attribute in ("status_code", "http_status", "status", "code"):
            value = getattr(error, attribute, None)
            if isinstance(value, int):
                return value

        return None

    @staticmethod
    def _resolve_message(
        *, message: str | None, error: Exception | None, status: int | None
    ) -> str:
        if message:
            return message
        if error is not None and str(error):
            return str(error)
        if status is not None:
            return f"Scryfall request failed with HTTP status {status}."
        return "Scryfall request failed."

    @staticmethod
    def _is_validation_error(error: Exception | None) -> bool:
        if error is None:
            return False
        return isinstance(error, (TypeError, ValueError))

    @staticmethod
    def _is_response_format_error(error: Exception | None) -> bool:
        if error is None:
            return False
        return isinstance(error, (KeyError, LookupError, AttributeError))
