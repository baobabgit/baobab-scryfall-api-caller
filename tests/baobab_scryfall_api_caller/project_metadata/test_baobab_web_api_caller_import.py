"""Verifie que la dependance runtime baobab-web-api-caller est importable."""

from __future__ import annotations


class TestBaobabWebApiCallerImport:
    """La couche de transport declaree doit etre presente dans l'environnement."""

    def test_core_public_symbols_exist(self) -> None:
        """Les symboles attendus pour composer le transport doivent exister."""
        import baobab_web_api_caller as bw

        assert hasattr(bw, "BaobabServiceCaller")
        assert hasattr(bw, "HttpTransportCaller")
        assert hasattr(bw, "ServiceConfig")
