"""Run CSV-based sales analytics and demonstrate every iterator/generator.

Completed sales contribute to revenue and product/category analytics.
The application processes data lazily rather than keeping all rows in memory.
"""

from itertools import islice
from pathlib import Path
from typing import Iterator

from generators.sales_generator import (
    calculate_revenue,
    filter_sales,
    generate_batches,
    generate_top_products,
    read_sales,
)
from iterators.sales_iterator import SalesIterator
from services.analytics import (
    Sale,
    calculate_average_check,
    calculate_total_revenue,
    count_sales,
    get_most_popular_product,
    get_most_profitable_category,
    get_top_products,
)


SALES_FILE: str = str(
    Path(__file__).resolve().parent / "data" / "sales.csv"
    )


def completed_sales() -> Iterator[Sale]:
    """Provide a fresh stream of completed sales for each calculation."""
    return filter_sales(read_sales(SALES_FILE), "completed")


def main() -> None:
    """Print a sales summary and demonstrate all processing components."""
    total_sales = count_sales(read_sales(SALES_FILE))
    completed_count = count_sales(completed_sales())
    total_revenue = calculate_total_revenue(completed_sales())
    average_check = calculate_average_check(completed_sales())
    most_popular_product = get_most_popular_product(completed_sales())
    most_profitable_category = get_most_profitable_category(completed_sales())
    top_products = get_top_products(completed_sales())

    print("========== SALES ANALYTICS ==========\n")
    print(f"Total sales: {total_sales}")
    print(f"Completed sales: {completed_count}")
    print(f"Total revenue: {total_revenue:.2f}")
    print(f"Average check: {average_check:.2f}")
    print(f"Most popular product: {most_popular_product}")
    print(f"Most profitable category: {most_profitable_category}")
    print("Top 5 products:")
    for index, (product, revenue) in enumerate(top_products, start=1):
        print(f"{index}. {product} - {revenue:.2f}")
    print("\n=====================================\n")

    print("========== COMPONENT DEMO ==========\n")
    print("SalesIterator (Electronics, first 3):")
    for sale in islice(SalesIterator(read_sales(SALES_FILE), "Electronics"), 3):
        print(f"  #{sale['id']} {sale['product']} - {sale['category']}")

    print("Cumulative completed revenue (first 3):")
    for revenue in islice(calculate_revenue(completed_sales()), 3):
        print(f"  {revenue:.2f}")

    print("Completed sales batches (sizes of first 2 batches):")
    for batch in islice(generate_batches(completed_sales(), 5), 2):
        print(f"  {len(batch)}")

    print("Product revenue pairs (first 3):")
    for product, revenue in islice(generate_top_products(completed_sales()), 3):
        print(f"  {product} - {revenue:.2f}")
    print("\n====================================")


if __name__ == "__main__":
    main()
