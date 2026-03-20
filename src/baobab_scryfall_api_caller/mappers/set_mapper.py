"""Mapper de payload set Scryfall vers objets metier."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.scryfall_payload_coercions import (
    as_bool,
    as_int,
    as_optional_int,
    as_optional_str,
)
from baobab_scryfall_api_caller.models.sets.set import Set


class SetMapper:
    """Mappe une reponse set brute vers `Set`."""

    def map_set(self, raw_set: Any) -> Set:
        """Transforme un payload Scryfall en modele `Set`."""
        if not isinstance(raw_set, dict):
            raise ScryfallResponseFormatException(
                "Set payload must be a dictionary.",
                response_detail=raw_set,
            )

        if raw_set.get("object") != "set":
            raise ScryfallResponseFormatException(
                "Set payload has an invalid 'object' field.",
                response_detail=raw_set,
            )

        set_id = raw_set.get("id")
        code = raw_set.get("code")
        name = raw_set.get("name")
        if not isinstance(set_id, str) or not set_id:
            raise ScryfallResponseFormatException(
                "Set payload is missing a valid 'id'.",
                response_detail=raw_set,
            )
        if not isinstance(code, str) or not code:
            raise ScryfallResponseFormatException(
                "Set payload is missing a valid 'code'.",
                response_detail=raw_set,
            )
        if not isinstance(name, str) or not name:
            raise ScryfallResponseFormatException(
                "Set payload is missing a valid 'name'.",
                response_detail=raw_set,
            )

        invalid_str = "Set payload contains an invalid string field."
        invalid_int = "Set payload contains an invalid integer field."
        invalid_bool = "Set payload contains an invalid boolean field."

        return Set(
            id=set_id,
            code=code,
            name=name,
            set_type=as_optional_str(
                raw_set.get("set_type"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
            released_at=as_optional_str(
                raw_set.get("released_at"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
            block_code=as_optional_str(
                raw_set.get("block_code"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
            block=as_optional_str(
                raw_set.get("block"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
            parent_set_code=as_optional_str(
                raw_set.get("parent_set_code"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
            card_count=as_int(
                raw_set.get("card_count"),
                default=0,
                invalid_message=invalid_int,
                response_detail=raw_set,
            ),
            printed_size=as_optional_int(
                raw_set.get("printed_size"),
                invalid_message=invalid_int,
                response_detail=raw_set,
            ),
            digital=as_bool(
                raw_set.get("digital"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_set,
            ),
            foil_only=as_bool(
                raw_set.get("foil_only"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_set,
            ),
            nonfoil_only=as_bool(
                raw_set.get("nonfoil_only"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_set,
            ),
            foil=as_bool(
                raw_set.get("foil"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_set,
            ),
            nonfoil=as_bool(
                raw_set.get("nonfoil"),
                default=False,
                invalid_message=invalid_bool,
                response_detail=raw_set,
            ),
            icon_svg_uri=as_optional_str(
                raw_set.get("icon_svg_uri"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
            search_uri=as_optional_str(
                raw_set.get("search_uri"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
            scryfall_uri=as_optional_str(
                raw_set.get("scryfall_uri"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
            uri=as_optional_str(
                raw_set.get("uri"),
                invalid_message=invalid_str,
                response_detail=raw_set,
            ),
        )
