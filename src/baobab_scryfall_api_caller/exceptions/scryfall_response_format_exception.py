"""Exception dediee aux formats de reponse inattendus."""

from baobab_scryfall_api_caller.exceptions.baobab_scryfall_api_caller_exception import (
    BaobabScryfallApiCallerException,
)


class ScryfallResponseFormatException(BaobabScryfallApiCallerException):
    """Erreur declenchee quand la structure de reponse ne respecte pas le contrat attendu."""
