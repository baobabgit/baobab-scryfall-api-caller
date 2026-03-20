"""Tests du mapper CardMapper."""

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers import CardMapper


class TestCardMapper:
    """Valide le mapping de payload carte."""

    def test_map_card_nominal(self) -> None:
        """Le mapping nominal doit produire un Card avec champs principaux."""
        mapper = CardMapper()
        card = mapper.map_card(
            {
                "id": "card-id",
                "name": "Black Lotus",
                "layout": "normal",
                "oracle_id": "oracle-id",
                "mtgo_id": 111,
                "cardmarket_id": 222,
                "set": "lea",
                "collector_number": "233",
            }
        )
        assert card.id == "card-id"
        assert card.name == "Black Lotus"
        assert card.set_code == "lea"
        assert card.collector_number == "233"

    def test_map_card_with_faces(self) -> None:
        """Le mapping doit prendre en charge les cartes multi-faces."""
        mapper = CardMapper()
        card = mapper.map_card(
            {
                "id": "card-id",
                "name": "Brisela, Voice of Nightmares",
                "card_faces": [
                    {"name": "Bruna, the Fading Light"},
                    {"name": "Gisela, the Broken Blade"},
                ],
            }
        )
        assert len(card.faces) == 2
        assert card.faces[0].name == "Bruna, the Fading Light"

    def test_map_card_missing_required_fields_raises(self) -> None:
        """Les champs obligatoires manquants doivent lever une erreur de format."""
        mapper = CardMapper()
        try:
            mapper.map_card({"name": "No id"})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_card_invalid_faces_raises(self) -> None:
        """Un champ card_faces invalide doit lever une erreur de format."""
        mapper = CardMapper()
        try:
            mapper.map_card({"id": "x", "name": "y", "card_faces": "invalid"})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"
