"""Exception dediee aux ressources Scryfall introuvables."""

from baobab_scryfall_api_caller.exceptions.scryfall_request_exception import (
    ScryfallRequestException,
)


class ScryfallNotFoundException(ScryfallRequestException):
    """Erreur declenchee quand Scryfall renvoie une absence de ressource."""
