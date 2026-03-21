"""Conversion d'une URL de telechargement bulk (absolue) en config baobab-web-api-caller."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from types import MappingProxyType
from urllib.parse import parse_qs, urlparse

from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException


def build_service_config_and_request_for_bulk_download(
    download_uri: str,
    *,
    default_headers: Mapping[str, str] | None = None,
) -> tuple[ServiceConfig, BaobabRequest]:
    """Construit ``ServiceConfig`` + ``BaobabRequest`` pour :class:`BulkFileDownloader`.

    Les URLs renvoyees par Scryfall sont absolues (souvent un autre hote que l'API).
    On isole l'origine (scheme + netloc) comme ``base_url`` et le chemin + query comme
    requete relative, comme attendu par ``baobab-web-api-caller``.

    :param download_uri: URL complete du fichier (champ ``download_uri`` de :class:`BulkData`).
    :param default_headers: Headers par defaut (ex. copie de ``ServiceConfig.default_headers``).
    :raises ScryfallValidationException: si l'URL est vide ou non utilisable.
    """
    if not isinstance(download_uri, str):
        raise ScryfallValidationException(
            "'download_uri' must be a string.",
            params={"download_uri": download_uri},
        )
    stripped = download_uri.strip()
    if not stripped:
        raise ScryfallValidationException(
            "'download_uri' cannot be empty.",
            params={"download_uri": download_uri},
        )

    parsed = urlparse(stripped)
    if parsed.scheme not in {"http", "https"}:
        raise ScryfallValidationException(
            "'download_uri' must use http or https.",
            params={"download_uri": download_uri},
        )
    if not parsed.netloc:
        raise ScryfallValidationException(
            "'download_uri' must include a host.",
            params={"download_uri": download_uri},
        )

    origin = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
    path = parsed.path if parsed.path else "/"
    if not path.startswith("/"):
        path = f"/{path}"

    raw_query = parse_qs(parsed.query, keep_blank_values=True)
    query_params: dict[str, str | Sequence[str]] = {}
    for key, values in raw_query.items():
        if len(values) == 1:
            query_params[key] = values[0]
        else:
            query_params[key] = values

    headers_frozen: Mapping[str, str] = (
        MappingProxyType(dict(default_headers)) if default_headers else MappingProxyType({})
    )

    try:
        service_config = ServiceConfig(base_url=origin, default_headers=headers_frozen)
    except ConfigurationException as exc:
        raise ScryfallValidationException(
            "Invalid download URL for bulk file transfer.",
            params={"download_uri": download_uri},
            cause=exc,
        ) from exc

    try:
        request = BaobabRequest(
            method=HttpMethod.GET,
            path=path,
            query_params=query_params,
            headers={},
        )
    except ConfigurationException as exc:
        raise ScryfallValidationException(
            "Invalid download URL path or query for bulk file transfer.",
            params={"download_uri": download_uri},
            cause=exc,
        ) from exc

    return service_config, request
