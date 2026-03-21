"""Verifie que la dependance runtime baobab-web-api-caller est installee."""

from __future__ import annotations

import importlib.metadata


class TestBaobabWebApiCallerDependency:
    """La couche de transport declaree doit etre presente dans l'environnement."""

    def test_distribution_is_installed(self) -> None:
        """Le wheel `baobab-web-api-caller` doit etre resolu (sans import du package).

        On evite `import baobab_web_api_caller` ici : l'import du paquet top-level
        execute `__init__.py` et depend de versions alignees ; la librairie
        `baobab-scryfall-api-caller` n'importe pas ce paquet au chargement des
        modules (injection du transport). La presence du wheel suffit pour la CI.
        """
        distribution = importlib.metadata.distribution("baobab-web-api-caller")
        assert distribution.version
        assert distribution.metadata["Name"] == "baobab-web-api-caller"
