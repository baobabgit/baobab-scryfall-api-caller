"""Package principal de la librairie baobab-scryfall-api-caller."""

from baobab_scryfall_api_caller.client.scryfall_api_caller import ScryfallApiCaller
from baobab_scryfall_api_caller.client.web_api_transport_protocol import WebApiTransportProtocol

__all__ = ["__version__", "ScryfallApiCaller", "WebApiTransportProtocol"]

__version__ = "0.2.0"
