"""Tests de CardCollectionIdentifier."""

from __future__ import annotations

from uuid import UUID

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException
from baobab_scryfall_api_caller.models.cards.card_collection_identifier import (
    CardCollectionIdentifier,
)


class TestCardCollectionIdentifier:
    """Valide les schemas d'identifiants collection."""

    def test_identifier_by_id(self) -> None:
        """Schema id + UUID canonique."""
        uid = "683a5707-cddb-494d-9b41-51b4584ded69"
        ident = CardCollectionIdentifier(id=uid)
        assert ident.to_api_dict() == {"id": str(UUID(uid))}

    def test_identifier_by_mtgo_id(self) -> None:
        """Schema mtgo_id seul."""
        ident = CardCollectionIdentifier(mtgo_id=12345)
        assert ident.to_api_dict() == {"mtgo_id": 12345}

    def test_identifier_by_multiverse_id(self) -> None:
        """Schema multiverse_id seul."""
        ident = CardCollectionIdentifier(multiverse_id=99)
        assert ident.to_api_dict() == {"multiverse_id": 99}

    def test_identifier_by_oracle_id(self) -> None:
        """Schema oracle_id."""
        oid = "00000000-0000-4000-8000-000000000099"
        ident = CardCollectionIdentifier(oracle_id=oid)
        assert ident.to_api_dict() == {"oracle_id": str(UUID(oid))}

    def test_identifier_by_illustration_id(self) -> None:
        """Schema illustration_id."""
        iid = "00000000-0000-4000-8000-000000000088"
        ident = CardCollectionIdentifier(illustration_id=iid)
        assert ident.to_api_dict() == {"illustration_id": str(UUID(iid))}

    def test_identifier_by_name(self) -> None:
        """Schema name seul."""
        ident = CardCollectionIdentifier(name="  Lightning Bolt  ")
        assert ident.to_api_dict() == {"name": "Lightning Bolt"}

    def test_identifier_by_name_and_set(self) -> None:
        """Schema name + set."""
        ident = CardCollectionIdentifier(name="Island", set_code="neo")
        assert ident.to_api_dict() == {"name": "Island", "set": "neo"}

    def test_identifier_by_set_and_collector(self) -> None:
        """Schema set + collector_number."""
        ident = CardCollectionIdentifier(set_code="mrd", collector_number="150")
        assert ident.to_api_dict() == {"collector_number": "150", "set": "mrd"}

    def test_missing_strategy_raises(self) -> None:
        """Sans strategie valide, construction impossible."""
        try:
            CardCollectionIdentifier()
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_multiple_strategies_raise(self) -> None:
        """Plusieurs strategies melangees doivent lever."""
        try:
            CardCollectionIdentifier(
                id="683a5707-cddb-494d-9b41-51b4584ded69",
                name="X",
            )
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_invalid_positive_int_raises(self) -> None:
        """mtgo_id non positif doit lever."""
        try:
            CardCollectionIdentifier(mtgo_id=0)
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_mtgo_id_wrong_type_raises(self) -> None:
        """mtgo_id non entier doit lever."""
        try:
            CardCollectionIdentifier(mtgo_id="1")  # type: ignore[arg-type]
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"

    def test_name_empty_after_strip_raises(self) -> None:
        """name uniquement vide apres strip doit lever."""
        try:
            CardCollectionIdentifier(name="   ")
        except ScryfallValidationException:
            assert True
        else:
            assert False, "Expected ScryfallValidationException"
