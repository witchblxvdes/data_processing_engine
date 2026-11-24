"""Lazy CSV reading and sales-processing generators."""

import csv
from typing import Iterable, Iterator

from services.analytics import Sale


def read_sales(filename: str) -> Iterator[Sale]:
    """Yield sales dictionaries from CSV, converting numeric fields.

    Args:
        filename: Path to a CSV file containing the six required headers.

    Yields:
        dict: A sale with integer id/quantity and float price.
    """
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield {
                "id": int(row["id"]),
                "product": row["product"],
                "category": row["category"],
                "quantity": int(row["quantity"]),
                "price": float(row["price"]),
                "status": row["status"],
            }


def filter_sales(
                  sales: Iterable[Sale],
                  status: str
                  ) -> Iterator[Sale]:
    """Yield only sales whose status matches the requested status."""
    for sale in sales:
        if sale["status"] == status:
            yield sale


def calculate_revenue(sales: Iterable[Sale]) -> Iterator[float]:
    """Yield the running revenue total after every sale."""
    total_revenue = 0.0
    for sale in sales:
        total_revenue += sale["quantity"] * sale["price"]
        yield total_revenue


def generate_batches(
                      sales: Iterable[Sale],
                      batch_size: int
                      ) -> Iterator[list[Sale]]:
    """Yield consecutive lists of at most batch_size sales.

    Raises:
        TypeError: If batch_size is not an integer (or is a bool).
        ValueError: If batch_size is not positive.
    """
    if not isinstance(batch_size, int) or isinstance(batch_size, bool):
        raise TypeError("Batch size must be an integer.")
    if batch_size <= 0:
        raise ValueError("Batch size must be greater than zero.")

    batch = []
    for sale in sales:
        batch.append(sale)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def generate_top_products(sales: Iterable[Sale]) -> Iterator[tuple[str, float]]:
    """Yield (product name, individual sale revenue) pairs for analysis."""
    for sale in sales:
        revenue = sale["quantity"] * sale["price"]
        yield (sale["product"], revenue)
