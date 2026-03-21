"""Tests de l'exception racine."""

from baobab_scryfall_api_caller.exceptions import BaobabScryfallApiCallerException


class TestBaobabScryfallApiCallerException:
    """Valide la construction et la serialisation de l'exception racine."""

    def test_metadata_are_stored(self) -> None:
        """Les metadonnees de diagnostic doivent etre conservees."""
        cause = RuntimeError("network down")
        exception = BaobabScryfallApiCallerException(
            "Erreur metier",
            http_status=503,
            url="https://api.scryfall.com/cards/random",
            params={"q": "t:angel"},
            payload={"foo": "bar"},
            response_detail={"object": "error"},
            cause=cause,
        )

        assert exception.message == "Erreur metier"
        assert exception.http_status == 503
        assert exception.url == "https://api.scryfall.com/cards/random"
        assert exception.params == {"q": "t:angel"}
        assert exception.payload == {"foo": "bar"}
        assert exception.response_detail == {"object": "error"}
        assert exception.cause is cause

    def test_str_includes_context_when_available(self) -> None:
        """Le texte doit inclure les informations utiles au diagnostic."""
        exception = BaobabScryfallApiCallerException(
            "Oops",
            http_status=404,
            url="https://api.scryfall.com/cards/unknown",
            params={"id": "unknown"},
        )
        rendered = str(exception)
        assert "Oops" in rendered
        assert "http_status=404" in rendered
        assert "url=https://api.scryfall.com/cards/unknown" in rendered
        assert "params={'id': 'unknown'}" in rendered

    def test_str_without_context_returns_message(self) -> None:
        """Sans contexte, le rendu textuel doit etre le message brut."""
        exception = BaobabScryfallApiCallerException("Erreur simple")
        assert str(exception) == "Erreur simple"

    def test_str_includes_payload_response_detail_and_cause(self) -> None:
        """Toutes les metadonnees optionnelles doivent apparaitre dans le rendu."""
        cause = ValueError("upstream")
        exception = BaobabScryfallApiCallerException(
            "Echec",
            payload={"a": 1},
            response_detail={"raw": True},
            cause=cause,
        )
        text = str(exception)
        assert "payload=" in text
        assert "response_detail=" in text
        assert "cause=" in text
