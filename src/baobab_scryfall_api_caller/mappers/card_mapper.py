"""Mapper de payload carte Scryfall vers objets metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.scryfall_payload_coercions import (
    as_bool,
    as_legalities_tuple,
    as_optional_float,
    as_optional_int,
    as_optional_str,
    as_string_tuple,
)
from baobab_scryfall_api_caller.models.cards.card import Card
from baobab_scryfall_api_caller.models.cards.card_face import CardFace
from baobab_scryfall_api_caller.models.cards.image_uris import ImageUris


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
        invalid_str = "Card payload contains an invalid string field."
        invalid_int = "Card payload contains an invalid integer field."
        invalid_bool = "Card payload contains an invalid boolean field."
        invalid_list = "Card payload contains an invalid list field."
        invalid_legal = "Card payload contains an invalid 'legalities' field."
        return Card(
            id=card_id,
            name=name,
            layout=as_optional_str(
                raw_card.get("layout"),
                invalid_message=invalid_str,
            ),
            oracle_id=as_optional_str(
                raw_card.get("oracle_id"),
                invalid_message=invalid_str,
            ),
            mtgo_id=as_optional_int(
                raw_card.get("mtgo_id"),
                invalid_message=invalid_int,
            ),
            cardmarket_id=as_optional_int(
                raw_card.get("cardmarket_id"),
                invalid_message=invalid_int,
            ),
            set_code=as_optional_str(
                raw_card.get("set"),
                invalid_message=invalid_str,
            ),
            collector_number=as_optional_str(
                raw_card.get("collector_number"),
                invalid_message=invalid_str,
            ),
            faces=faces,
            type_line=as_optional_str(
                raw_card.get("type_line"),
                invalid_message=invalid_str,
            ),
            oracle_text=as_optional_str(
                raw_card.get("oracle_text"),
                invalid_message=invalid_str,
            ),
            rarity=as_optional_str(
                raw_card.get("rarity"),
                invalid_message=invalid_str,
            ),
            cmc=as_optional_float(
                raw_card.get("cmc"),
                invalid_message="Card payload contains an invalid 'cmc' field.",
                response_detail=raw_card,
            ),
            colors=as_string_tuple(
                raw_card.get("colors"),
                invalid_message=invalid_list,
                response_detail=raw_card,
            ),
            color_identity=as_string_tuple(
                raw_card.get("color_identity"),
                invalid_message=invalid_list,
                response_detail=raw_card,
            ),
            lang=as_optional_str(
                raw_card.get("lang"),
                invalid_message=invalid_str,
            ),
            artist=as_optional_str(
                raw_card.get("artist"),
                invalid_message=invalid_str,
            ),
            flavor_text=as_optional_str(
                raw_card.get("flavor_text"),
                invalid_message=invalid_str,
            ),
            image_uris=self._map_image_uris(raw_card.get("image_uris"), raw_card),
            reserved=as_bool(
                raw_card.get("reserved"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_card,
            ),
            foil=as_bool(
                raw_card.get("foil"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_card,
            ),
            nonfoil=as_bool(
                raw_card.get("nonfoil"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_card,
            ),
            digital=as_bool(
                raw_card.get("digital"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_card,
            ),
            games=as_string_tuple(
                raw_card.get("games"),
                invalid_message=invalid_list,
                response_detail=raw_card,
            ),
            legalities=as_legalities_tuple(
                raw_card.get("legalities"),
                invalid_message=invalid_legal,
                response_detail=raw_card,
            ),
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
                    loyalty=as_optional_str(
                        raw_face.get("loyalty"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    defense=as_optional_str(
                        raw_face.get("defense"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    flavor_text=as_optional_str(
                        raw_face.get("flavor_text"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    artist=as_optional_str(
                        raw_face.get("artist"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    illustration_id=as_optional_str(
                        raw_face.get("illustration_id"),
                        invalid_message="Card payload contains an invalid string field.",
                    ),
                    image_uris=self._map_image_uris(raw_face.get("image_uris"), raw_card),
                )
            )
        return tuple(faces)

    @staticmethod
    def _map_image_uris(raw: Any, response_detail: dict[str, Any]) -> ImageUris | None:
        if raw is None:
            return None
        if not isinstance(raw, dict):
            raise ScryfallResponseFormatException(
                "Card payload has an invalid 'image_uris' object.",
                response_detail=response_detail,
            )
        invalid_str = "Card payload contains an invalid string field in 'image_uris'."
        return ImageUris(
            small=as_optional_str(raw.get("small"), invalid_message=invalid_str),
            normal=as_optional_str(raw.get("normal"), invalid_message=invalid_str),
            large=as_optional_str(raw.get("large"), invalid_message=invalid_str),
            png=as_optional_str(raw.get("png"), invalid_message=invalid_str),
            art_crop=as_optional_str(raw.get("art_crop"), invalid_message=invalid_str),
            border_crop=as_optional_str(raw.get("border_crop"), invalid_message=invalid_str),
        )
