"""Coherence version et exports publics pour la release."""

from __future__ import annotations

import importlib.metadata
import re

import baobab_scryfall_api_caller as root_package
from baobab_scryfall_api_caller import __version__


def test_version_matches_distribution_metadata() -> None:
    """La version importable doit correspondre au package installe (wheel ou editable)."""
    dist_version = importlib.metadata.version("baobab-scryfall-api-caller")
    assert dist_version == __version__
    assert __version__
    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__), "Version semver simple attendue"


def test_root_all_exports() -> None:
    """Exports publics documentes du package racine."""
    assert set(root_package.__all__) == {
        "__version__",
        "ScryfallApiCaller",
        "WebApiTransportProtocol",
    }
