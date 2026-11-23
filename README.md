# Data Processing Engine

A Python learning project for streaming-style sales analysis with custom iterators, generators, and CSV files.

## Features

- Read sales records lazily from CSV with `read_sales()`.
- Filter sales by status with `filter_sales()`.
- Iterate over any sales iterable (including a generator), optionally selecting a category, using `SalesIterator`.
- Yield cumulative revenue with `calculate_revenue()`.
- Yield batches of a given positive size with `generate_batches()`.
- Yield `(product, revenue)` pairs per sale with `generate_top_products()`.
- Calculate sales counts, total revenue, average check, most popular product by units, highest-revenue category and top five products by revenue.

## Project structure

```text
data_processing_engine/
├── data/
│   └── sales.csv
├── iterators/
│   ├── __init__.py
│   └── sales_iterator.py
├── generators/
│   ├── __init__.py
│   └── sales_generator.py
├── services/
│   ├── __init__.py
│   └── analytics.py
├── main.py
├── .gitignore
└── README.md
```

## Requirements

Python 3.10 or newer. No third-party packages are needed.

## Getting started

Run from the project directory:

```bash
python main.py
```

The included `data/sales.csv` contains 100 sample records. To regenerate sample data (overwriting the file), run:

```bash
python generate_data.py
```

You can launch `main.py` from another working directory because its CSV path is based on the location of the Python source file.

## CSV schema

The CSV file must have these headers:

| Field | Type | Example |
|---|---|---|
| `id` | int | `1` |
| `product` | str | `Laptop` |
| `category` | str | `Electronics` |
| `quantity` | int | `2` |
| `price` | float | `1200.0` |
| `status` | str | `completed` |

Sample statuses: `completed`, `pending`, `cancelled`.

## Analytics rules

- **Total sales** counts all records.
- **Completed sales** counts only `status == "completed"`.
- All revenue, average check, product and category rankings in `main.py` use **completed sales only**.
- The most popular product is determined by *units sold*, while top products and top category are determined by *revenue* (`quantity * price`).
- The average check is revenue divided by number of sales, or `0` when empty.
- All analytics use a fresh generator: a previously consumed generator cannot be reused without recreating it.

## Iterator vs. generator

`read_sales()` returns a **generator object**. Each yielded sale is a **dictionary**. `SalesIterator` can accept an iterable (such as a list or that generator); internally, `iter(sales)` creates an iterator and `next()` fetches matching records until `StopIteration`.

```python
from generators.sales_generator import read_sales
from iterators.sales_iterator import SalesIterator

sales = read_sales("data/sales.csv")
iterator = SalesIterator(sales, category="Electronics")
for sale in iterator:
    print(sale["product"])
```

## Memory usage

CSV reading, filtering, and running totals operate incrementally instead of loading every record into a list. `generate_batches()` stores at most `batch_size` records. Product and category rankings store aggregate information for each **unique** item/category, so memory usage depends on the number of unique keys. Sorting the product ranking also allocates a list of unique products.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Sample output

The program prints `SALES ANALYTICS` statistics followed by a `COMPONENT DEMO` that exercises the custom iterator and all five generators. Exact statistics depend on the CSV contents.
