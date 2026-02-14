"""
computeSales.py

Computes the total cost of sales based on a product price catalogue
and a sales record file in JSON format.
"""

import json
import sys
import time
from typing import Dict, List


def load_product_catalogue(filename: str) -> Dict[str, float]:
    """
    Loads the product catalogue and returns a dictionary
    with product title as key and price as value.
    """
    catalogue = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

            for item in data:
                try:
                    title = item["title"]
                    price = float(item["price"])
                    catalogue[title] = price
                except (KeyError, ValueError, TypeError) as error:
                    print(f"Invalid product entry skipped: {error}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")

    return catalogue


def load_sales(filename: str) -> List[dict]:
    """
    Loads the sales records from a JSON file.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")

    return []


def compute_total_sales(
    catalogue: Dict[str, float],
    sales: List[dict]
) -> float:
    """
    Computes the total sales amount.
    """
    total = 0.0

    for sale in sales:
        try:
            product = sale["Product"]
            quantity = int(sale["Quantity"])

            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            if product not in catalogue:
                print(f"Product not found in catalogue: {product}")
                continue

            total += catalogue[product] * quantity

        except (KeyError, ValueError, TypeError) as error:
            print(f"Invalid sale record skipped: {error}")

    return total


def save_results(total: float, elapsed_time: float) -> None:
    """
    Saves the results to SalesResults.txt.
    """
    with open("SalesResults.txt", "w", encoding="utf-8") as file:
        file.write("Sales Results\n")
        file.write("----------------------------\n")
        file.write(f"Total sales amount: ${total:.2f}\n")
        file.write(f"Execution time: {elapsed_time:.6f} seconds\n")


def main() -> None:
    """
    Main execution function.
    """
    if len(sys.argv) != 3:
        print(
            "Usage: python computeSales.py "
            "priceCatalogue.json salesRecord.json"
        )
        sys.exit(1)

    start_time = time.time()

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    catalogue = load_product_catalogue(catalogue_file)
    sales = load_sales(sales_file)

    total = compute_total_sales(catalogue, sales)

    elapsed_time = time.time() - start_time

    print("\nSales Results")
    print("----------------------------")
    print(f"Total sales amount: ${total:.2f}")
    print(f"Execution time: {elapsed_time:.6f} seconds")

    save_results(total, elapsed_time)


if __name__ == "__main__":
    main()