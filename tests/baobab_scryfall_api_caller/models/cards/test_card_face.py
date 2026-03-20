"""Tests du modele CardFace."""

from baobab_scryfall_api_caller.models.cards import CardFace


class TestCardFace:
    """Valide la structure du modele CardFace."""

    def test_nominal_construction(self) -> None:
        """La construction nominale doit conserver les champs."""
        face = CardFace(
            name="Bruna, the Fading Light",
            mana_cost="{5}{W}{W}",
            type_line="Legendary Creature — Angel Horror",
            oracle_text="Flying, vigilance",
            power="5",
            toughness="7",
        )
        assert face.name == "Bruna, the Fading Light"
        assert face.mana_cost == "{5}{W}{W}"
        assert face.power == "5"
        assert face.toughness == "7"
