"""Exception dediee aux erreurs de requete vers Scryfall."""

from baobab_scryfall_api_caller.exceptions.baobab_scryfall_api_caller_exception import (
    BaobabScryfallApiCallerException,
)


class ScryfallRequestException(BaobabScryfallApiCallerException):
    """Erreur de transport ou HTTP renvoyee lors d'un appel Scryfall."""
