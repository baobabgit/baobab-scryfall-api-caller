"""Mapper de payload ruling Scryfall vers objets metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.models.rulings.ruling import Ruling


class RulingMapper:
    """Mappe une reponse ruling brute vers `Ruling`."""

    def map_ruling(self, raw_ruling: Any) -> Ruling:
        """Transforme un objet ruling Scryfall en modele `Ruling`."""
        if not isinstance(raw_ruling, dict):
            raise ScryfallResponseFormatException(
                "Ruling payload must be a dictionary.",
                response_detail=raw_ruling,
            )

        if raw_ruling.get("object") != "ruling":
            raise ScryfallResponseFormatException(
                "Ruling payload has an invalid 'object' field.",
                response_detail=raw_ruling,
            )

        oracle_id = raw_ruling.get("oracle_id")
        source = raw_ruling.get("source")
        published_at = raw_ruling.get("published_at")
        comment = raw_ruling.get("comment")

        if not isinstance(oracle_id, str) or not oracle_id:
            raise ScryfallResponseFormatException(
                "Ruling payload is missing a valid 'oracle_id'.",
                response_detail=raw_ruling,
            )
        if not isinstance(source, str) or not source:
            raise ScryfallResponseFormatException(
                "Ruling payload is missing a valid 'source'.",
                response_detail=raw_ruling,
            )
        if not isinstance(published_at, str) or not published_at:
            raise ScryfallResponseFormatException(
                "Ruling payload is missing a valid 'published_at'.",
                response_detail=raw_ruling,
            )
        if not isinstance(comment, str):
            raise ScryfallResponseFormatException(
                "Ruling payload is missing a valid 'comment'.",
                response_detail=raw_ruling,
            )

        return Ruling(
            oracle_id=oracle_id,
            source=source,
            published_at=published_at,
            comment=comment,
        )
