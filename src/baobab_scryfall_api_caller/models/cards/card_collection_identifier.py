"""Identifiant de carte pour la requete POST /cards/collection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.validation.scryfall_request_validators import (
    ScryfallRequestValidators,
)


@dataclass(frozen=True)
class CardCollectionIdentifier:  # pylint: disable=too-many-instance-attributes
    """Identifiant unitaire conforme aux schemas Scryfall pour /cards/collection.

    Utiliser un seul groupe de champs parmi les strategies supportees :
    ``id``, ``mtgo_id``, ``multiverse_id``, ``oracle_id``, ``illustration_id``,
    ``name`` seul, ``name`` + ``set_code``, ou ``set_code`` + ``collector_number``.

    Le champ ``set_code`` est serialise en ``set`` dans le JSON Scryfall.
    """

    id: str | None = None
    mtgo_id: int | None = None
    multiverse_id: int | None = None
    oracle_id: str | None = None
    illustration_id: str | None = None
    name: str | None = None
    set_code: str | None = None
    collector_number: str | None = None

    def __post_init__(self) -> None:
        """Valide qu'un seul schema d'identification est respecte."""
        self._validate_schema()

    def to_api_dict(self) -> dict[str, Any]:  # pylint: disable=too-many-return-statements
        """Produit l'objet JSON attendu dans ``identifiers``."""
        if self.id is not None:
            return {
                "id": ScryfallRequestValidators.require_uuid_string(value=self.id, field_name="id")
            }
        if self.mtgo_id is not None:
            return {
                "mtgo_id": ScryfallRequestValidators.require_strict_positive_int(
                    value=self.mtgo_id,
                    field_name="mtgo_id",
                )
            }
        if self.multiverse_id is not None:
            return {
                "multiverse_id": ScryfallRequestValidators.require_strict_positive_int(
                    value=self.multiverse_id,
                    field_name="multiverse_id",
                )
            }
        if self.oracle_id is not None:
            return {
                "oracle_id": ScryfallRequestValidators.require_uuid_string(
                    value=self.oracle_id,
                    field_name="oracle_id",
                )
            }
        if self.illustration_id is not None:
            return {
                "illustration_id": ScryfallRequestValidators.require_uuid_string(
                    value=self.illustration_id,
                    field_name="illustration_id",
                )
            }
        if self.name is not None and self.set_code is not None:
            return {
                "name": ScryfallRequestValidators.require_non_empty_text(
                    value=self.name,
                    field_name="name",
                ),
                "set": ScryfallRequestValidators.require_non_empty_text(
                    value=self.set_code,
                    field_name="set_code",
                ),
            }
        if self.name is not None:
            return {
                "name": ScryfallRequestValidators.require_non_empty_text(
                    value=self.name,
                    field_name="name",
                )
            }
        if self.set_code is not None and self.collector_number is not None:
            return {
                "set": ScryfallRequestValidators.require_non_empty_text(
                    value=self.set_code,
                    field_name="set_code",
                ),
                "collector_number": ScryfallRequestValidators.require_non_empty_text(
                    value=self.collector_number,
                    field_name="collector_number",
                ),
            }
        raise AssertionError("Unreachable: schema validated in __post_init__.")  # pragma: no cover

    def _validate_schema(self) -> None:
        """Verifie la coherence des champs non nuls."""
        non_none = {
            field: value
            for field, value in (
                ("id", self.id),
                ("mtgo_id", self.mtgo_id),
                ("multiverse_id", self.multiverse_id),
                ("oracle_id", self.oracle_id),
                ("illustration_id", self.illustration_id),
                ("name", self.name),
                ("set_code", self.set_code),
                ("collector_number", self.collector_number),
            )
            if value is not None
        }
        keys = set(non_none.keys())
        if not keys:
            raise ScryfallValidationException(
                "CardCollectionIdentifier cannot be empty.",
                params={"identifier": self},
            )
        allowed = (
            {"id"},
            {"mtgo_id"},
            {"multiverse_id"},
            {"oracle_id"},
            {"illustration_id"},
            {"name"},
            {"name", "set_code"},
            {"set_code", "collector_number"},
        )
        if keys not in allowed:
            raise ScryfallValidationException(
                "Invalid card collection identifier: use a single supported schema "
                "(id, mtgo_id, multiverse_id, oracle_id, illustration_id, name, "
                "name+set_code, or set_code+collector_number).",
                params={"fields": sorted(keys)},
            )
        if self.id is not None:
            ScryfallRequestValidators.require_uuid_string(value=self.id, field_name="id")
        if self.mtgo_id is not None:
            ScryfallRequestValidators.require_strict_positive_int(
                value=self.mtgo_id,
                field_name="mtgo_id",
            )
        if self.multiverse_id is not None:
            ScryfallRequestValidators.require_strict_positive_int(
                value=self.multiverse_id,
                field_name="multiverse_id",
            )
        if self.oracle_id is not None:
            ScryfallRequestValidators.require_uuid_string(
                value=self.oracle_id, field_name="oracle_id"
            )
        if self.illustration_id is not None:
            ScryfallRequestValidators.require_uuid_string(
                value=self.illustration_id,
                field_name="illustration_id",
            )
        if self.name is not None:
            ScryfallRequestValidators.require_non_empty_text(value=self.name, field_name="name")
        if self.set_code is not None:
            ScryfallRequestValidators.require_non_empty_text(
                value=self.set_code,
                field_name="set_code",
            )
        if self.collector_number is not None:
            ScryfallRequestValidators.require_non_empty_text(
                value=self.collector_number,
                field_name="collector_number",
            )
