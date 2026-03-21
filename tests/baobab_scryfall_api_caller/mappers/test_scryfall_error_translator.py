"""Tests du traducteur d'erreurs Scryfall."""

from baobab_scryfall_api_caller.exceptions import (
    ScryfallBulkDataException,
    ScryfallNotFoundException,
    ScryfallPaginationException,
    ScryfallRateLimitException,
    ScryfallRequestException,
    ScryfallResponseFormatException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.mappers import ErrorTranslationContext, ScryfallErrorTranslator


class TestScryfallErrorTranslator:
    """Valide la traduction de plusieurs scenarios d'erreur."""

    def test_translates_http_404_to_not_found(self) -> None:
        """HTTP 404 doit etre mappe vers ScryfallNotFoundException."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(
            error=RuntimeError("Not found"),
            context=ErrorTranslationContext(http_status=404),
        )
        assert isinstance(translated, ScryfallNotFoundException)
        assert translated.http_status == 404

    def test_translates_http_429_to_rate_limit(self) -> None:
        """HTTP 429 doit etre mappe vers ScryfallRateLimitException."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(
            error=RuntimeError("Rate limit"),
            context=ErrorTranslationContext(http_status=429),
        )
        assert isinstance(translated, ScryfallRateLimitException)
        assert translated.http_status == 429

    def test_translates_validation_error(self) -> None:
        """ValueError doit etre mappe vers ScryfallValidationException."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(error=ValueError("invalid query"))
        assert isinstance(translated, ScryfallValidationException)
        assert translated.cause is not None

    def test_translates_response_format_error(self) -> None:
        """KeyError doit etre mappe vers ScryfallResponseFormatException."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(error=KeyError("missing data"))
        assert isinstance(translated, ScryfallResponseFormatException)

    def test_forced_category_translation(self) -> None:
        """La categorie explicite doit prendre le pas sur l'heuristique."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(
            context=ErrorTranslationContext(
                category="pagination",
                message="Invalid page token",
            )
        )
        assert isinstance(translated, ScryfallPaginationException)
        assert translated.message == "Invalid page token"

    def test_bulk_data_forced_category(self) -> None:
        """La categorie bulk_data doit produire l'exception dediee."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(
            context=ErrorTranslationContext(
                category="bulk_data",
                response_detail={"type": "oracle_cards"},
            )
        )
        assert isinstance(translated, ScryfallBulkDataException)
        assert translated.response_detail == {"type": "oracle_cards"}

    def test_falls_back_to_request_exception(self) -> None:
        """Sans signal particulier, le fallback doit etre ScryfallRequestException."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(error=RuntimeError("Connection aborted"))
        assert isinstance(translated, ScryfallRequestException)

    def test_handles_missing_values(self) -> None:
        """Le traducteur doit etre robuste quand les valeurs sont absentes."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate()
        assert isinstance(translated, ScryfallRequestException)
        assert translated.http_status is None
        assert translated.url is None
        assert translated.message == "Scryfall request failed."

    def test_default_message_includes_route_for_http_status(self) -> None:
        """Sans message explicite, le statut HTTP doit mentionner la route si connue."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(
            context=ErrorTranslationContext(
                http_status=502,
                url="/bulk-data",
            ),
        )
        assert translated.message == (
            "Scryfall request failed with HTTP status 502. Route: /bulk-data."
        )

    def test_default_message_includes_route_without_status(self) -> None:
        """Route seule : message dedie (ex. contexte incomplet)."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(
            context=ErrorTranslationContext(
                url="/cards/search",
            ),
        )
        assert translated.message == "Scryfall request failed (route: /cards/search)."

    def test_uses_explicit_message_and_context(self) -> None:
        """Le message et le contexte explicites doivent etre conserves."""
        translator = ScryfallErrorTranslator()
        translated = translator.translate(
            error=RuntimeError("Original cause"),
            context=ErrorTranslationContext(
                message="Custom message",
                http_status=500,
                url="https://api.scryfall.com/cards/search",
                params={"q": "t:dragon"},
                payload={"foo": "bar"},
                response_detail={"object": "error"},
            ),
        )

        assert translated.message == "Custom message"
        assert translated.http_status == 500
        assert translated.url == "https://api.scryfall.com/cards/search"
        assert translated.params == {"q": "t:dragon"}
        assert translated.payload == {"foo": "bar"}
        assert translated.response_detail == {"object": "error"}
        assert translated.cause is not None
