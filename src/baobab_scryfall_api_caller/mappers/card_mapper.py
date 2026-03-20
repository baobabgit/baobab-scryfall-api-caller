"""Mapper de payload carte Scryfall vers objets metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.scryfall_payload_coercions import (
    as_optional_int,
    as_optional_str,
)
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
            layout=as_optional_str(
                raw_card.get("layout"),
                invalid_message="Card payload contains an invalid string field.",
            ),
            oracle_id=as_optional_str(
                raw_card.get("oracle_id"),
                invalid_message="Card payload contains an invalid string field.",
            ),
            mtgo_id=as_optional_int(
                raw_card.get("mtgo_id"),
                invalid_message="Card payload contains an invalid integer field.",
            ),
            cardmarket_id=as_optional_int(
                raw_card.get("cardmarket_id"),
                invalid_message="Card payload contains an invalid integer field.",
            ),
            set_code=as_optional_str(
                raw_card.get("set"),
                invalid_message="Card payload contains an invalid string field.",
            ),
            collector_number=as_optional_str(
                raw_card.get("collector_number"),
                invalid_message="Card payload contains an invalid string field.",
            ),
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
                    mana_cost=as_optional_str(
                        raw_face.get("mana_cost"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    type_line=as_optional_str(
                        raw_face.get("type_line"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    oracle_text=as_optional_str(
                        raw_face.get("oracle_text"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    power=as_optional_str(
                        raw_face.get("power"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    toughness=as_optional_str(
                        raw_face.get("toughness"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                )
            )
        return tuple(faces)
