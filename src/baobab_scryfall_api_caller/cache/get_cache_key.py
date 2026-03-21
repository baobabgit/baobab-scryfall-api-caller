"""Cle stable pour indexer les reponses GET dans le cache."""

from __future__ import annotations

import json
from typing import Any


def make_get_cache_key(*, route: str, params: dict[str, Any] | None) -> str:
    """Construit une cle a partir du chemin et des parametres de requete GET."""
    normalized_route = route if route.startswith("/") else f"/{route}"
    if not params:
        return f"GET|{normalized_route}|"
    payload = json.dumps(params, sort_keys=True, separators=(",", ":"))
    return f"GET|{normalized_route}|{payload}"
