"""Normalisation des query params Scryfall vers le modele attendu par baobab-web-api-caller."""

from __future__ import annotations

from typing import Any, Sequence


class BaobabQueryParamsNormalizer:
    """Convertit les dictionnaires de parametres Scryfall en query string compatibles.

    `baobab-web-api-caller` attend des valeurs ``str`` ou des sequences de ``str`` ;
    les entiers et autres types simples sont convertis en chaines.
    """

    @staticmethod
    def normalize(params: dict[str, Any] | None) -> dict[str, str | Sequence[str]] | None:
        """Retourne ``None`` si ``params`` est absent, sinon un mapping normalise."""
        if params is None:
            return None
        normalized: dict[str, str | Sequence[str]] = {}
        for key, value in params.items():
            if isinstance(value, (list, tuple)):
                normalized[key] = [str(item) for item in value]
            else:
                normalized[key] = str(value)
        return normalized
