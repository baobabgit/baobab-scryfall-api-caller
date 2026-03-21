"""Tests de iter_list_pages / iter_list_items."""

from __future__ import annotations

import pytest

from baobab_scryfall_api_caller.models.common import ListResponse, PaginationMetadata
from baobab_scryfall_api_caller.pagination import iter_list_items, iter_list_pages


class TestListResponseFollow:
    """Iteration explicite sur les pages reliees par next_page."""

    def test_single_page_no_follow(self) -> None:
        """Sans has_more, une seule page est parcourue."""
        first = ListResponse[str](
            data=["a"],
            metadata=PaginationMetadata(has_more=False),
        )
        pages = list(iter_list_pages(first, fetch_next=_fail_if_called))
        assert len(pages) == 1
        assert pages[0] is first

    def test_two_pages(self) -> None:
        """fetch_next est appele une fois pour la deuxieme page."""
        second = ListResponse[str](
            data=["c"],
            metadata=PaginationMetadata(has_more=False),
        )

        def fetch_next(url: str) -> ListResponse[str]:
            assert url == "https://example/next"
            return second

        first = ListResponse[str](
            data=["a", "b"],
            metadata=PaginationMetadata(
                has_more=True,
                next_page="https://example/next",
            ),
        )
        out = list(iter_list_pages(first, fetch_next=fetch_next))
        assert len(out) == 2
        assert out[0] is first
        assert out[1] is second

    def test_max_pages_stops_early(self) -> None:
        """max_pages borne le nombre de pages yield."""
        first = ListResponse[int](
            data=[1],
            metadata=PaginationMetadata(
                has_more=True,
                next_page="https://example/next",
            ),
        )
        calls = 0

        def fetch_next(_url: str) -> ListResponse[int]:
            nonlocal calls
            calls += 1
            return ListResponse[int](
                data=[2],
                metadata=PaginationMetadata(
                    has_more=True,
                    next_page="https://example/next2",
                ),
            )

        pages = list(iter_list_pages(first, fetch_next=fetch_next, max_pages=1))
        assert len(pages) == 1
        assert calls == 0

    def test_iter_list_items_flattens(self) -> None:
        """iter_list_items enchaine les elements de chaque page."""
        first = ListResponse[str](
            data=["a"],
            metadata=PaginationMetadata(
                has_more=True,
                next_page="u2",
            ),
        )

        def fetch_next(url: str) -> ListResponse[str]:
            assert url == "u2"
            return ListResponse[str](
                data=["b"],
                metadata=PaginationMetadata(has_more=False),
            )

        assert list(iter_list_items(first, fetch_next=fetch_next)) == ["a", "b"]

    def test_iter_list_items_respects_max_pages(self) -> None:
        """max_pages limite aussi les elements parcourus."""
        first = ListResponse[str](
            data=["a", "b"],
            metadata=PaginationMetadata(
                has_more=True,
                next_page="https://x",
            ),
        )

        def fetch_next(_url: str) -> ListResponse[str]:
            return ListResponse[str](
                data=["c"],
                metadata=PaginationMetadata(has_more=False),
            )

        assert list(iter_list_items(first, fetch_next=fetch_next, max_pages=1)) == ["a", "b"]


def _fail_if_called(_url: str) -> ListResponse[str]:
    pytest.fail("fetch_next should not be called")
