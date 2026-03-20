"""Exports publics des exceptions metier du projet."""

from baobab_scryfall_api_caller.exceptions.baobab_scryfall_api_caller_exception import (
    BaobabScryfallApiCallerException,
)
from baobab_scryfall_api_caller.exceptions.scryfall_bulk_data_exception import (
    ScryfallBulkDataException,
)
from baobab_scryfall_api_caller.exceptions.scryfall_not_found_exception import (
    ScryfallNotFoundException,
)
from baobab_scryfall_api_caller.exceptions.scryfall_pagination_exception import (
    ScryfallPaginationException,
)
from baobab_scryfall_api_caller.exceptions.scryfall_rate_limit_exception import (
    ScryfallRateLimitException,
)
from baobab_scryfall_api_caller.exceptions.scryfall_request_exception import (
    ScryfallRequestException,
)
from baobab_scryfall_api_caller.exceptions.scryfall_response_format_exception import (
    ScryfallResponseFormatException,
)
from baobab_scryfall_api_caller.exceptions.scryfall_validation_exception import (
    ScryfallValidationException,
)

__all__ = [
    "BaobabScryfallApiCallerException",
    "ScryfallRequestException",
    "ScryfallNotFoundException",
    "ScryfallValidationException",
    "ScryfallRateLimitException",
    "ScryfallResponseFormatException",
    "ScryfallPaginationException",
    "ScryfallBulkDataException",
]
