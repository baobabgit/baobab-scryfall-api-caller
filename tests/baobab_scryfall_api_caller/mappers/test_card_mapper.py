"""Tests du mapper CardMapper."""

from baobab_scryfall_api_caller.exceptions import ScryfallResponseFormatException
from baobab_scryfall_api_caller.mappers import CardMapper
from baobab_scryfall_api_caller.models.cards import ImageUris


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

    def test_map_card_enrichment_fields(self) -> None:
        """Champs typiques Scryfall supplementaires (gameplay, legalites, images)."""
        mapper = CardMapper()
        card = mapper.map_card(
            {
                "id": "c1",
                "name": "Lightning Bolt",
                "type_line": "Instant",
                "oracle_text": "Deal 3 damage to any target.",
                "rarity": "common",
                "cmc": 1,
                "colors": ["R"],
                "color_identity": ["R"],
                "lang": "en",
                "artist": "Artist",
                "flavor_text": "Flavor",
                "reserved": False,
                "foil": True,
                "nonfoil": True,
                "digital": False,
                "games": ["paper", "mtgo"],
                "legalities": {"modern": "legal", "legacy": "legal"},
                "image_uris": {
                    "small": "https://x/small.jpg",
                    "normal": "https://x/normal.jpg",
                },
            }
        )
        assert card.type_line == "Instant"
        assert card.oracle_text == "Deal 3 damage to any target."
        assert card.rarity == "common"
        assert card.cmc == 1.0
        assert card.colors == ("R",)
        assert card.color_identity == ("R",)
        assert card.lang == "en"
        assert card.artist == "Artist"
        assert card.flavor_text == "Flavor"
        assert card.foil is True
        assert card.games == ("paper", "mtgo")
        assert card.legalities == (("legacy", "legal"), ("modern", "legal"))
        assert isinstance(card.image_uris, ImageUris)
        assert card.image_uris.small == "https://x/small.jpg"

    def test_map_card_partial_payload_no_regression(self) -> None:
        """Les reponses minimales ne doivent pas exiger les nouveaux champs."""
        mapper = CardMapper()
        card = mapper.map_card({"id": "c1", "name": "X"})
        assert card.colors == ()
        assert card.legalities == ()
        assert card.image_uris is None

    def test_map_card_invalid_colors_raises(self) -> None:
        """Une liste de couleurs mal formee doit lever."""
        mapper = CardMapper()
        try:
            mapper.map_card({"id": "c1", "name": "X", "colors": ["R", 1]})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_card_invalid_legalities_raises(self) -> None:
        """Legalites non dict doivent lever."""
        mapper = CardMapper()
        try:
            mapper.map_card({"id": "c1", "name": "X", "legalities": "oops"})
        except ScryfallResponseFormatException:
            assert True
        else:
            assert False, "Expected ScryfallResponseFormatException"

    def test_map_card_face_enrichment(self) -> None:
        """Faces d'une carte DFC avec champs supplementaires."""
        mapper = CardMapper()
        card = mapper.map_card(
            {
                "id": "dfc",
                "name": "Arlinn",
                "card_faces": [
                    {
                        "name": "Arlinn Kord",
                        "loyalty": "3",
                        "flavor_text": "Day",
                        "artist": "A",
                        "image_uris": {"png": "https://x/p.png"},
                    },
                    {
                        "name": "Arlinn, Embraced by the Moon",
                        "defense": "4",
                    },
                ],
            }
        )
        assert card.faces[0].loyalty == "3"
        assert card.faces[0].flavor_text == "Day"
        assert card.faces[0].image_uris is not None
        assert card.faces[0].image_uris.png == "https://x/p.png"
        assert card.faces[1].defense == "4"
