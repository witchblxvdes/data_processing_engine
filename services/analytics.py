"""One-pass sales analytics using iterables rather than materialized records."""

from typing import Iterable, TypedDict

class Sale(TypedDict):
    """Represent a sales record with typed fields."""

    id: int
    product: str
    category: str
    quantity: int
    price: float
    status: str

def count_sales(sales: Iterable[Sale]) -> int:
    """Return the number of records in sales."""
    total = 0
    for _sale in sales:
        total += 1
    return total


def calculate_total_revenue(sales: Iterable[Sale]) -> float:
    """Return the total revenue across the supplied sales."""
    total_revenue = 0.0
    for sale in sales:
        total_revenue += sale["quantity"] * sale["price"]
    return total_revenue


def calculate_average_check(sales: Iterable[Sale]) -> float:
    """Return revenue per sale, or zero when there are no sales."""
    total_sales = 0
    total_revenue = 0.0
    for sale in sales:
        total_sales += 1
        total_revenue += sale["quantity"] * sale["price"]
    if total_sales == 0:
        return 0.0
    return total_revenue / total_sales


def get_most_popular_product(sales: Iterable[Sale]) -> str | None:
    """Return the product with the greatest number of units sold, or None."""
    product_counts = {}
    for sale in sales:
        product = sale["product"]
        product_counts[product] = product_counts.get(product, 0) + sale["quantity"]
    if not product_counts:
        return None
    return max(product_counts, key=lambda product: product_counts[product])


def get_most_profitable_category(sales: Iterable[Sale]) -> str | None:
    """Return the category with the greatest total revenue, or None."""
    category_revenue = {}
    for sale in sales:
        category = sale["category"]
        revenue = sale["quantity"] * sale["price"]
        category_revenue[category] = category_revenue.get(category, 0) + revenue
    if not category_revenue:
        return None
    return max(category_revenue, key=lambda category: category_revenue[category])


def get_top_products(sales: Iterable[Sale]) -> list[tuple[int, float]]:
    """Return up to five (product, total revenue) pairs in descending order."""
    product_revenue = {}
    for sale in sales:
        product = sale["product"]
        revenue = sale["quantity"] * sale["price"]
        product_revenue[product] = product_revenue.get(product, 0) + revenue
    sorted_products = sorted(product_revenue.items(), key=lambda item: item[1], reverse=True)
    return sorted_products[:5]
