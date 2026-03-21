"""Tests du module cache (cle, predicat, memoire)."""

from __future__ import annotations

from baobab_scryfall_api_caller.cache import (
    InMemoryJsonCache,
    default_cacheable_get,
    make_get_cache_key,
)


class TestMakeGetCacheKey:
    """Cles stables pour indexation."""

    def test_same_params_same_key(self) -> None:
        """Ordre des cles JSON trie."""
        a = make_get_cache_key(route="/sets", params={"page": 2})
        b = make_get_cache_key(route="/sets", params={"page": 2})
        assert a == b

    def test_params_order_irrelevant(self) -> None:
        """Tri des cles JSON dans la cle."""
        a = make_get_cache_key(route="/sets", params={"page": 2, "x": 1})
        b = make_get_cache_key(route="/sets", params={"x": 1, "page": 2})
        assert a == b


class TestDefaultCacheableGet:
    """Liste conservative de routes GET."""

    def test_catalog_bulk_sets_rulings_uuid(self) -> None:
        """Chemins typiques autorises."""
        assert default_cacheable_get("/catalog/card-names", None) is True
        assert default_cacheable_get("/bulk-data", None) is True
        assert default_cacheable_get("/sets", None) is True
        assert default_cacheable_get("/sets/neo", None) is True
        assert (
            default_cacheable_get(
                "/cards/00000000-0000-4000-8000-000000000001/rulings",
                None,
            )
            is True
        )
        assert (
            default_cacheable_get(
                "/cards/00000000-0000-4000-8000-000000000001",
                None,
            )
            is True
        )

    def test_excludes_search_and_random(self) -> None:
        """Endpoints dynamiques non caches par defaut."""
        assert default_cacheable_get("/cards/search", {"q": "x"}) is False
        assert default_cacheable_get("/cards/random", None) is False
        assert default_cacheable_get("/cards/autocomplete", {"q": "a"}) is False


class TestInMemoryJsonCache:
    """Copies defensives et clear."""

    def test_get_returns_copy(self) -> None:
        """Mutation du retour n'altere pas le stockage."""
        cache = InMemoryJsonCache()
        payload = {"object": "catalog", "data": ["a"]}
        cache.set("k", payload)
        out = cache.get("k")
        assert out is not None
        out["data"].append("b")
        out2 = cache.get("k")
        assert out2 is not None
        assert out2["data"] == ["a"]

    def test_clear(self) -> None:
        """Reinitialisation explicite."""
        cache = InMemoryJsonCache()
        cache.set("k", {"x": 1})
        cache.clear()
        assert cache.get("k") is None
