"""Identifiants et requetes stables pour les tests d'integration Scryfall.

Ces valeurs proviennent de l'API publique documentee (exemples officiels ou cartes
d'extension Judgment) et visent a limiter la fragilite des assertions.
"""

# Exemple documente dans la doc Scryfall GET /cards/:id (carte Judgment).
DOC_EXAMPLE_CARD_ID = "56ebc372-aabd-4174-a943-c7bf59e5028d"

# Deuxieme carte Judgment (liste e:jud, unique=cards) pour POST /cards/collection.
JUDGMENT_SECOND_CARD_ID = "c0cf71e1-3c57-47f9-a4ef-e0d0ad1ee329"

# Set connu pour get_by_code / list_sets (Kamigawa: Neon Dynasty).
KNOWN_SET_CODE = "neo"

# Requete de recherche large pour exercer la pagination (types de creatures).
SEARCH_QUERY_BROAD = "t:creature"

# Prefixe autocomplete (noms de cartes frequentes).
AUTOCOMPLETE_QUERY = "light"

# Catalogue generique (GET /catalog/{key}) — cles stables documentees Scryfall.
CATALOG_KEY_CREATURE_TYPES = "creature-types"

# Type bulk courant (GET /bulk-data/{type}).
BULK_TYPE_ORACLE_CARDS_SLUG = "oracle-cards"
