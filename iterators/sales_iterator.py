"""Custom iterator for sequential sales records and optional category filtering."""

from typing import Iterable, Iterator, Self

from services.analytics import Sale


class SalesIterator:
    """Iterate over any iterable of sales dictionaries.

    Args:
        sales: An iterable of sales records (including generators).
        category: Optional category to include; None includes all categories.

    The underlying iterable is consumed as the iterator advances.
    """

    def __init__(self, sales: Iterable[Sale], category: str | None = None) -> None:
        self.sales: Iterator[Sale] = iter(sales)
        self.category: str | None = category

    def __iter__(self)  -> Self:
        """Return this iterator."""
        return self

    def __next__(self) -> Sale:
        """Return the next matching sale, or raise StopIteration at the end."""
        for sale in self.sales:
            if self.category is None or sale["category"] == self.category:
                return sale
        raise StopIteration
