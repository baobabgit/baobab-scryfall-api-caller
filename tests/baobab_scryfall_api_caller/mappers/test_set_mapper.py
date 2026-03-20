"""Tests du mapper SetMapper."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.set_mapper import SetMapper
from baobab_scryfall_api_caller.models.sets.set import Set


def _minimal_valid_set_payload(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "object": "set",
        "id": "2f601c3a-3c97-4b47-9bfc-6d37dc2c7f8f",
        "code": "neo",
        "name": "Kamigawa: Neon Dynasty",
        "set_type": "expansion",
        "released_at": "2022-02-18",
        "card_count": 302,
        "digital": False,
        "foil_only": False,
        "nonfoil_only": False,
        "foil": True,
        "nonfoil": True,
    }
    base.update(overrides)
    return base


class TestSetMapper:
    """Valide le mapping des payloads set."""

    def test_map_set_nominal(self) -> None:
        """Un payload minimal valide doit produire un Set."""
        mapper = SetMapper()
        payload = _minimal_valid_set_payload()
        result = mapper.map_set(payload)
        assert isinstance(result, Set)
        assert result.id == payload["id"]
        assert result.code == "neo"
        assert result.name == payload["name"]
        assert result.card_count == 302

    def test_map_set_rejects_non_dict(self) -> None:
        """Un type non dict doit lever une erreur de format."""
        mapper = SetMapper()
        try:
            mapper.map_set("bad")
        except ScryfallResponseFormatException as exception:
            assert "dictionary" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_set_rejects_wrong_object_field(self) -> None:
        """Un objet autre que 'set' doit etre rejete."""
        mapper = SetMapper()
        payload = _minimal_valid_set_payload(object="list")
        try:
            mapper.map_set(payload)
        except ScryfallResponseFormatException as exception:
            assert "object" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_set_missing_id(self) -> None:
        """Un id manquant doit etre rejete."""
        mapper = SetMapper()
        payload = _minimal_valid_set_payload(id="")
        try:
            mapper.map_set(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_set_invalid_boolean_field(self) -> None:
        """Un champ booleen invalide doit etre rejete."""
        mapper = SetMapper()
        payload = _minimal_valid_set_payload(digital="yes")
        try:
            mapper.map_set(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_set_invalid_code_type(self) -> None:
        """Un code non chaine doit etre rejete."""
        mapper = SetMapper()
        payload = _minimal_valid_set_payload(code=123)
        try:
            mapper.map_set(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_set_invalid_optional_string_field(self) -> None:
        """Un champ texte optionnel invalide doit etre rejete."""
        mapper = SetMapper()
        payload = _minimal_valid_set_payload(set_type=[])
        try:
            mapper.map_set(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
