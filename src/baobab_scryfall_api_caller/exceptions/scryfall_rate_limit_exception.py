"""Exception dediee au depassement des limites de requetes."""

from baobab_scryfall_api_caller.exceptions.scryfall_request_exception import (
    ScryfallRequestException,
)


class ScryfallRateLimitException(ScryfallRequestException):
    """Erreur declenchee quand l'API retourne un statut de limitation."""
