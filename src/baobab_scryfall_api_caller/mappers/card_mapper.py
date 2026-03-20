"""Mapper de payload carte Scryfall vers objets metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.models.cards.card import Card
from baobab_scryfall_api_caller.models.cards.card_face import CardFace


class CardMapper:
    """Mappe une reponse carte brute vers `Card`."""

    def map_card(self, raw_card: Any) -> Card:
        """Transforme un payload Scryfall en modele `Card`."""
        if not isinstance(raw_card, dict):
            raise ScryfallResponseFormatException(
                "Card payload must be a dictionary.",
                response_detail=raw_card,
            )

        card_id = raw_card.get("id")
        name = raw_card.get("name")
        if not isinstance(card_id, str) or not card_id:
            raise ScryfallResponseFormatException(
                "Card payload is missing a valid 'id'.",
                response_detail=raw_card,
            )
        if not isinstance(name, str) or not name:
            raise ScryfallResponseFormatException(
                "Card payload is missing a valid 'name'.",
                response_detail=raw_card,
            )

        faces = self._map_faces(raw_card.get("card_faces"), raw_card)
        return Card(
            id=card_id,
            name=name,
            layout=self._as_optional_str(raw_card.get("layout")),
            oracle_id=self._as_optional_str(raw_card.get("oracle_id")),
            mtgo_id=self._as_optional_int(raw_card.get("mtgo_id")),
            cardmarket_id=self._as_optional_int(raw_card.get("cardmarket_id")),
            set_code=self._as_optional_str(raw_card.get("set")),
            collector_number=self._as_optional_str(raw_card.get("collector_number")),
            faces=faces,
        )

    def _map_faces(self, raw_faces: Any, raw_card: dict[str, Any]) -> tuple[CardFace, ...]:
        if raw_faces is None:
            return ()
        if not isinstance(raw_faces, list):
            raise ScryfallResponseFormatException(
                "Card payload has an invalid 'card_faces' field.",
                response_detail=raw_card,
            )

        faces: list[CardFace] = []
        for raw_face in raw_faces:
            if not isinstance(raw_face, dict):
                raise ScryfallResponseFormatException(
                    "Card face payload must be a dictionary.",
                    response_detail=raw_face,
                )
            face_name = raw_face.get("name")
            if not isinstance(face_name, str) or not face_name:
                raise ScryfallResponseFormatException(
                    "Card face payload is missing a valid 'name'.",
                    response_detail=raw_face,
                )
            faces.append(
                CardFace(
                    name=face_name,
                    mana_cost=self._as_optional_str(raw_face.get("mana_cost")),
                    type_line=self._as_optional_str(raw_face.get("type_line")),
                    oracle_text=self._as_optional_str(raw_face.get("oracle_text")),
                    power=self._as_optional_str(raw_face.get("power")),
                    toughness=self._as_optional_str(raw_face.get("toughness")),
                )
            )
        return tuple(faces)

    @staticmethod
    def _as_optional_str(value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, str):
            return value
        raise ScryfallResponseFormatException(
            "Card payload contains an invalid string field.",
            response_detail=value,
        )

    @staticmethod
    def _as_optional_int(value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        raise ScryfallResponseFormatException(
            "Card payload contains an invalid integer field.",
            response_detail=value,
        )
