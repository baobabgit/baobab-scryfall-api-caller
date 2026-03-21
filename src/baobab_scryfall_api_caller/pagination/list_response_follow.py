"""Iteration explicite sur les pages Scryfall reliees par ``next_page``.

Aucun appel HTTP n'est effectue ici : le consommateur fournit ``fetch_next``, qui
doit utiliser la meme chaine de transport que le reste de l'application
(``baobab-web-api-caller``).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import TypeVar

from baobab_scryfall_api_caller.models.common.list_response import ListResponse

T = TypeVar("T")


def iter_list_pages(
    first: ListResponse[T],
    *,
    fetch_next: Callable[[str], ListResponse[T]],
    max_pages: int | None = None,
) -> Iterator[ListResponse[T]]:
    """Yield la page initiale puis les suivantes via ``fetch_next(url)``.

    ``fetch_next`` recoit l'URL absolue ``next_page`` renvoyee par Scryfall ; elle doit
    declencher le GET (via ``ScryfallHttpClient`` / services) et retourner un
    ``ListResponse`` parse. Tant que cette fonction n'est pas appelee, aucune
    requete supplementaire n'est emise.

    :param first: premiere page deja obtenue (ex. retour de ``CardsService.search``).
    :param fetch_next: charge la page suivante a partir de l'URL ``next_page``.
    :param max_pages: borne optionnelle du nombre de pages parcourues (la premiere compte).
    """
    page: ListResponse[T] | None = first
    pages_seen = 0
    while page is not None:
        pages_seen += 1
        yield page
        if max_pages is not None and pages_seen >= max_pages:
            return
        if not page.has_more or not page.next_page:
            return
        page = fetch_next(page.next_page)


def iter_list_items(
    first: ListResponse[T],
    *,
    fetch_next: Callable[[str], ListResponse[T]],
    max_pages: int | None = None,
) -> Iterator[T]:
    """Yield tous les elements page par page (meme contrat que :func:`iter_list_pages`)."""
    for page in iter_list_pages(first, fetch_next=fetch_next, max_pages=max_pages):
        yield from page
