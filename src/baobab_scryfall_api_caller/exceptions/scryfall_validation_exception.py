"""Exception dediee aux erreurs de validation locale."""

from baobab_scryfall_api_caller.exceptions.baobab_scryfall_api_caller_exception import (
    BaobabScryfallApiCallerException,
)


class ScryfallValidationException(BaobabScryfallApiCallerException):
    """Erreur declenchee quand des entrees ne respectent pas le contrat metier."""
