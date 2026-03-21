"""Construction optionnelle de requetes pour le DSL de recherche Scryfall.

Les fragments produits sont concatenees par des espaces (AND implicite Scryfall).
Pour un controle total, utilisez :meth:`raw` ou passez une chaine brute a
:meth:`~baobab_scryfall_api_caller.services.cards.cards_service.CardsService.search`
via ``q=...``.
"""

from __future__ import annotations

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)

_CMC_OPS = frozenset({"=", "<", ">", "<=", ">="})


class CardSearchQuery:
    """Assemble des criteres courants en une chaine compatible avec ``GET /cards/search``.

    Exemple::

        q = CardSearchQuery().type_line("Creature").cmc(3).to_query_string()
        # "t:Creature cmc=3"
    """

    __slots__ = ("_terms",)

    def __init__(self) -> None:
        """Initialise un assembleur vide."""
        self._terms: list[str] = []

    def raw(self, dsl_fragment: str) -> CardSearchQuery:
        """Ajoute un fragment DSL tel quel (non vide apres strip).

        Utile pour tout operateur Scryfall non couvert par les helpers.
        """
        normalized = ScryfallRequestValidators.require_non_empty_text(
            value=dsl_fragment,
            field_name="dsl_fragment",
        )
        self._terms.append(normalized)
        return self

    def type_line(self, text: str) -> CardSearchQuery:
        """Critere ``t:`` (ligne de type)."""
        normalized = ScryfallRequestValidators.require_non_empty_text(
            value=text,
            field_name="type_line",
        )
        self._terms.append(f"t:{normalized}")
        return self

    def oracle(self, text: str) -> CardSearchQuery:
        """Critere ``o:`` (texte oracle)."""
        normalized = ScryfallRequestValidators.require_non_empty_text(
            value=text,
            field_name="oracle",
        )
        self._terms.append(f"o:{normalized}")
        return self

    def name_contains(self, text: str) -> CardSearchQuery:
        """Critere ``name:`` (nom partiel ou expression supportee par Scryfall)."""
        normalized = ScryfallRequestValidators.require_non_empty_text(
            value=text,
            field_name="name",
        )
        self._terms.append(f"name:{normalized}")
        return self

    def set_code(self, code: str) -> CardSearchQuery:
        """Critere ``s:`` (code d'extension, normalise en minuscules)."""
        normalized = ScryfallRequestValidators.require_non_empty_text(
            value=code,
            field_name="set_code",
        )
        self._terms.append(f"s:{normalized.lower()}")
        return self

    def cmc(self, value: int, *, op: str = "=") -> CardSearchQuery:
        """Critere ``cmc`` avec operateur ``=``, ``<``, ``>``, ``<=``, ``>=``."""
        if not isinstance(value, int):
            raise ScryfallValidationException(
                "'cmc' value must be an integer.",
                params={"value": value},
            )
        if op not in _CMC_OPS:
            raise ScryfallValidationException(
                f"'op' must be one of {sorted(_CMC_OPS)}.",
                params={"op": op},
            )
        self._terms.append(f"cmc{op}{value}")
        return self

    def to_query_string(self) -> str:
        """Produit la chaine transmise a Scryfall (espaces entre criteres)."""
        if not self._terms:
            raise ScryfallValidationException(
                "CardSearchQuery has no criteria; add terms or use a raw 'q' string.",
                params={"terms": self._terms},
            )
        return " ".join(self._terms)

    def build(self) -> str:
        """Alias de :meth:`to_query_string`."""
        return self.to_query_string()

    def __repr__(self) -> str:
        return f"CardSearchQuery({self._terms!r})"
