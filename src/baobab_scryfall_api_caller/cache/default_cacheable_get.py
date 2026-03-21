"""Selection des GET susceptibles d'etre mis en cache (liste conservative)."""

from __future__ import annotations

from typing import Any


def default_cacheable_get(route: str, params: dict[str, Any] | None) -> bool:
    """Retourne True pour des lectures relativement stables.

    Couvre notamment catalogs, sets, bulk, rulings, carte par UUID.
    Exclut explicitement la recherche, l'autocomplete, le hasard, la collection, etc.
    """
    _ = params
    r = route if route.startswith("/") else f"/{route}"
    if r.startswith("/catalog/"):
        return True
    if r.startswith("/bulk-data"):
        return True
    if r.startswith("/sets"):
        return True
    if r.startswith("/cards/") and "/rulings" in r:
        return True
    if r.startswith("/cards/"):
        first_segment = r[len("/cards/") :].split("/")[0]
        if len(first_segment) == 36 and first_segment.count("-") == 4:
            return True
    return False
