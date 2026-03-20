"""Exception dediee aux erreurs de metadonnees bulk data."""

from baobab_scryfall_api_caller.exceptions.baobab_scryfall_api_caller_exception import (
    BaobabScryfallApiCallerException,
)


class ScryfallBulkDataException(BaobabScryfallApiCallerException):
    """Erreur declenchee lors du traitement des datasets bulk."""
