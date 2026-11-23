"""Custom iterator for sequential sales records and optional category filtering."""


class SalesIterator:
    """Iterate over any iterable of sales dictionaries.

    Args:
        sales: An iterable of sales records (including generators).
        category: Optional category to include; None includes all categories.

    The underlying iterable is consumed as the iterator advances.
    """

    def __init__(self, sales, category=None) -> None:
        self.sales = iter(sales)
        self.category = category

    def __iter__(self):
        """Return this iterator."""
        return self

    def __next__(self):
        """Return the next matching sale, or raise StopIteration at the end."""
        for sale in self.sales:
            if self.category is None or sale["category"] == self.category:
                return sale
        raise StopIteration
