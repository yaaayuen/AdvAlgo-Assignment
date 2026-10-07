"""Command-line pharmacy inventory system built on the HashTable"""

from datetime import date

from hash_table import HashTable
from product import Product

TABLE_CAPACITY = 101

PRELOADED_PRODUCTS = [
    Product(1001, "Paracetamol 500mg", "5.90", 120, "Painkiller", date(2027, 6, 30)),
    Product(1002, "Ibuprofen 200mg", "8.50", 80, "Painkiller", date(2027, 3, 31)),
    Product(1003, "Amoxicillin 250mg", "15.00", 40, "Antibiotic", date(2026, 12, 31)),
    Product(1004, "Cetirizine 10mg", "12.90", 60, "Antihistamine", date(2027, 9, 30)),
    Product(1005, "Omeprazole 20mg", "18.50", 35, "Antacid", date(2027, 1, 31)),
    Product(1006, "Vitamin C 1000mg", "25.00", 150, "Supplement", date(2028, 2, 28)),
    Product(1007, "Loratadine 10mg", "11.20", 45, "Antihistamine", date(2027, 5, 31)),
    Product(1102, "Metformin 500mg", "9.80", 70, "Diabetes", date(2027, 8, 31)),
    Product(1203, "Salbutamol Inhaler", "22.00", 25, "Respiratory", date(2027, 4, 30)),
    Product(1304, "Oral Rehydration Salts", "3.50", 200, "Digestive", date(2028, 1, 31))
]

def load_preload(table):
    """Insert the preloaded products and show which slot each one used"""
    print("Loading preloaded products...")
    for product in PRELOADED_PRODUCTS:
        slot = table.insert(product.product_id, product)
        _, probes = table.locate(product.product_id)
        note = f" (collision: {probes} probes)" if probes > 1 else ""
        print(f"{product.product_id} {product.name:<24} ->  slot {slot:>3}{note}")

    print(f"{len(table)} products loaded. Load factor: {table.load_factor():.2f}\n")

if __name__ == "__main__":
    inventory = HashTable(TABLE_CAPACITY)
    load_preload(inventory)