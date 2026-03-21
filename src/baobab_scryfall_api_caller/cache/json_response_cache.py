"""Cache optionnel de payloads JSON (reponses Scryfall deja parsees en dict)."""

from __future__ import annotations

import copy
import threading
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class JsonResponseCache(Protocol):
    """Contrat minimal pour un cache de dictionnaires JSON (GET reussis)."""

    def get(self, key: str) -> dict[str, Any] | None:
        """Retourne une copie du payload mis en cache ou ``None``."""

    def set(self, key: str, value: dict[str, Any]) -> None:
        """Enregistre une copie du payload."""


class InMemoryJsonCache:
    """Cache processus-local en memoire (aucune persistance disque).

    Thread-safe ; les valeurs sont copiees a l'entree et a la sortie pour limiter
    les effets de bord si un appelant mute le dict retourne.
    """

    __slots__ = ("_data", "_lock")

    def __init__(self) -> None:
        self._data: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> dict[str, Any] | None:
        """Voir :meth:`JsonResponseCache.get`."""
        with self._lock:
            stored = self._data.get(key)
            if stored is None:
                return None
            return copy.deepcopy(stored)

    def set(self, key: str, value: dict[str, Any]) -> None:
        """Voir :meth:`JsonResponseCache.set`."""
        with self._lock:
            self._data[key] = copy.deepcopy(value)

    def clear(self) -> None:
        """Vide le cache (tests ou reinitialisation explicite)."""
        with self._lock:
            self._data.clear()
