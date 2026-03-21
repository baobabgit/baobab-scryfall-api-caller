"""Tests du mapper RulingMapper."""

from __future__ import annotations

from typing import Any

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers.ruling_mapper import RulingMapper
from baobab_scryfall_api_caller.models.rulings.ruling import Ruling


def _valid_ruling_payload(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "object": "ruling",
        "oracle_id": "abcdef01-2345-6789-abcd-ef0123456789",
        "source": "wotc",
        "published_at": "2007-02-01",
        "comment": "Example ruling text.",
    }
    base.update(overrides)
    return base


class TestRulingMapper:
    """Valide le mapping des payloads ruling."""

    def test_map_ruling_nominal(self) -> None:
        """Un payload valide doit produire un Ruling."""
        mapper = RulingMapper()
        payload = _valid_ruling_payload()
        result = mapper.map_ruling(payload)
        assert isinstance(result, Ruling)
        assert result.oracle_id == payload["oracle_id"]
        assert result.source == "wotc"
        assert result.comment == payload["comment"]
        assert result.ruling_id is None

    def test_map_ruling_with_record_id(self) -> None:
        """Le champ API ``id`` est expose en ``ruling_id``."""
        mapper = RulingMapper()
        rid = "11111111-1111-4111-8111-111111111111"
        payload = _valid_ruling_payload(id=rid)
        result = mapper.map_ruling(payload)
        assert result.ruling_id == rid

    def test_map_ruling_rejects_non_dict(self) -> None:
        """Un type non dict doit lever une erreur de format."""
        mapper = RulingMapper()
        try:
            mapper.map_ruling([])
        except ScryfallResponseFormatException as exception:
            assert "dictionary" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_ruling_wrong_object(self) -> None:
        """Un objet autre que ruling doit etre rejete."""
        mapper = RulingMapper()
        payload = _valid_ruling_payload(object="card")
        try:
            mapper.map_ruling(payload)
        except ScryfallResponseFormatException as exception:
            assert "object" in exception.message
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_ruling_missing_oracle_id(self) -> None:
        """Un oracle_id manquant doit etre rejete."""
        mapper = RulingMapper()
        payload = _valid_ruling_payload(oracle_id="")
        try:
            mapper.map_ruling(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_ruling_missing_source(self) -> None:
        """Une source manquante doit etre rejetee."""
        mapper = RulingMapper()
        payload = _valid_ruling_payload(source="")
        try:
            mapper.map_ruling(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_ruling_invalid_comment_type(self) -> None:
        """Un commentaire non chaine doit etre rejete."""
        mapper = RulingMapper()
        payload = _valid_ruling_payload(comment=None)
        try:
            mapper.map_ruling(payload)
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
