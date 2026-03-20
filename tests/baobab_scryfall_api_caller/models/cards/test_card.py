"""Tests du modele Card."""

from baobab_scryfall_api_caller.models.cards import Card, CardFace


class TestCard:
    """Valide le modele Card."""

    def test_nominal_construction_with_optional_fields(self) -> None:
        """Le modele doit conserver les champs mappes et optionnels."""
        card = Card(
            id="00000000-0000-0000-0000-000000000000",
            name="Sample Card",
            layout="normal",
            oracle_id="11111111-1111-1111-1111-111111111111",
            mtgo_id=12345,
            cardmarket_id=9999,
            set_code="lea",
            collector_number="233",
            faces=(CardFace(name="Sample Face"),),
        )
        assert card.id == "00000000-0000-0000-0000-000000000000"
        assert card.name == "Sample Card"
        assert card.layout == "normal"
        assert card.mtgo_id == 12345
        assert card.cardmarket_id == 9999
        assert len(card.faces) == 1
