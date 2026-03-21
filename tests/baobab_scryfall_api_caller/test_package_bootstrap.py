"""Tests de bootstrap du package principal."""

import baobab_scryfall_api_caller


class TestPackageBootstrap:
    """Valide l'import et les elements publics minimaux du package."""

    def test_package_import(self) -> None:
        """Le package doit etre importable."""
        assert baobab_scryfall_api_caller is not None

    def test_package_version_is_defined(self) -> None:
        """La version publique doit etre definie."""
        assert baobab_scryfall_api_caller.__version__ == "0.2.0"
