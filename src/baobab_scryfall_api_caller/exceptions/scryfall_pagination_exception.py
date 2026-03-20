"""Exception dediee aux erreurs de pagination Scryfall."""

from baobab_scryfall_api_caller.exceptions.baobab_scryfall_api_caller_exception import (
    BaobabScryfallApiCallerException,
)


class ScryfallPaginationException(BaobabScryfallApiCallerException):
    """Erreur declenchee quand la pagination Scryfall est invalide ou incoherente."""
