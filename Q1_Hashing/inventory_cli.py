"""Command-line pharmacy inventory system built on the HashTable"""

from datetime import date
from decimal import Decimal, InvalidOperation

from hash_table import HashTable
from product import Product

TABLE_CAPACITY = 101

PRELOADED_PRODUCTS = [
    Product(1001, "Paracetamol 500mg", "5.90", 120, "Painkiller", date(2027, 6, 30)),
    Product(1002, "Ibuprofen 200mg", "8.50", 80, "Painkiller", date(2027, 3, 31)),
    Product(1003, "Amoxicillin 250mg", "15.00", 40, "Antibiotic", date(2026, 12, 31), True),
    Product(1004, "Cetirizine 10mg", "12.90", 60, "Antihistamine", date(2027, 9, 30)),
    Product(1005, "Omeprazole 20mg", "18.50", 35, "Antacid", date(2027, 1, 31), True),
    Product(1006, "Vitamin C 1000mg", "25.00", 150, "Supplement", date(2028, 2, 28)),
    Product(1007, "Loratadine 10mg", "11.20", 45, "Antihistamine", date(2027, 5, 31)),
    Product(1102, "Metformin 500mg", "9.80", 70, "Diabetes", date(2027, 8, 31), True),
    Product(1203, "Salbutamol Inhaler", "22.00", 25, "Respiratory", date(2027, 4, 30), True),
    Product(1304, "Oral Rehydration Salts", "3.50", 200, "Digestive", date(2028, 1, 31))
]


def load_preloaded(table):
    """Insert the preloaded products and show which slot each one used"""
    print("Loading preloaded products...")
    for product in PRELOADED_PRODUCTS:
        slot = table.insert(product.product_id, product)
        _, probes = table.locate(product.product_id)
        note = f" (collision: {probes} probes)" if probes > 1 else ""
        print(f"{product.product_id} {product.name:<24} ->  slot {slot:>3}{note}")

    print(f"{len(table)} products loaded. Load factor: {table.load_factor():.2f}\n")


def read_int(prompt, minimum=None):
    """Keep asking until the user types a whole number"""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print("Please enter a whole number")
            continue
        if minimum is not None and value < minimum:
            print(f"Please enter a number of at least {minimum}")
            continue
        return value


def read_text(prompt):
    """Keep asking until the user types something that is not blank"""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be empty")


def read_price(prompt):
    """Keep asking until the user types a valid price"""
    while True:
        text = input(prompt).strip()
        try:
            price = Decimal(text)
        except InvalidOperation:
            print("Please enter a valid price")
            continue
        if not price.is_finite() or price < 0:
            print("Price must be 0 or more")
            continue
        return price


def read_date(prompt):
    """Keep asking until the user types a valid date (YYYY-MM-DD)"""
    while True:
        text = input(prompt).strip()
        try:
            return date.fromisoformat(text)
        except ValueError:
            print("Please enter a real date in YYYY-MM-DD format")


def read_yes_no(prompt):
    """Keep asking until the user types a y or n. Return True for y"""
    while True:
        text = input(prompt).strip().lower()
        if text in ("y", "yes"):
            return True
        if text in ("n", "no"):
            return False
        print("Please enter y or n")


def print_menu():
    """Show the main menu options"""
    print("==== Pharmacy Inventory System ====")
    print("1. Insert Product")
    print("2. Search Product")
    print("3. Edit Product")
    print("4. Delete Product")
    print("5. Display Hash Table")
    print("6. Exit")


def insert_product(table):
    """Ask for a new product's details and insert it into the table"""
    product_id = read_int("Product ID: ", minimum=1)
    if table.locate(product_id)[0] is not None:
        print(f"Product {product_id} already exists\n")
        return
    name = read_text("Enter Product Name: ")
    price = read_price("Enter Price (RM): ")
    stock = read_int("Enter Stock Quantity: ", minimum=0)
    category = read_text("Enter Product Category: ")
    expiry = read_date("Enter Expiry date (YYYY-MM-DD): ")
    if expiry <= date.today():
        print("This product expires today or has already expired, so it was not added\n")
        return
    needs_rx = read_yes_no("Needs prescription? (y/n): ")

    try:
        product = Product(product_id, name, price, stock, category, expiry, needs_rx)
        slot = table.insert(product_id, product)
    except (ValueError, OverflowError) as error:
        print(f"Could not insert product: {error}\n")
        return
    print(f"Product {product_id} inserted successfully into slot [{slot}]\n")


def search_product(table):
    """Ask for a Product ID and show the product if it exists"""
    product_id = read_int("Enter Product ID to search: ", minimum=1)
    slot, probes = table.locate(product_id)
    if slot is None:
        print(f"Product {product_id} not found (checked {probes} slot(s))\n")
        return
    product = table.search(product_id)
    print("Product found")
    print(product)
    print(f"Found in slot [{slot}] after {probes} probe(s)\n")


def edit_product(table):
    """Change the price and stock of an existing product"""
    product_id = read_int("Enter Product ID to edit: ", minimum=1)
    try:
        old = table.search(product_id)
    except KeyError:
        print(f"Product {product_id} not found\n")
        return
    print("Current:", old)
    price = read_price("Enter new Price (RM): ")
    stock = read_int("Enter new Stock Quantity: ", minimum=0)

    updated = Product(old.product_id, old.name, price, stock, old.category, old.expiry_date, old.requires_prescription)
    table.update(product_id, updated)
    print(f"Product updated: {updated}\n")


def delete_product(table):
    """Delete an existing product after the user confirms"""
    product_id = read_int("Enter Product ID to delete: ", minimum=1)
    try:
        product = table.search(product_id)
    except KeyError:
        print(f"Product {product_id} not found\n")
        return
    if not read_yes_no(f"Do you want to delete {product.name}? (y/n): "):
        print("Delete cancelled\n")
        return
    table.delete(product_id)
    print(f"Deleted: {product.name}\n")


def main():
    """Load the preloaded products, then run the menu until the user exits"""
    inventory = HashTable(TABLE_CAPACITY)
    load_preloaded(inventory)

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            insert_product(inventory)
        elif choice == "2":
            search_product(inventory)
        elif choice == "3":
            edit_product(inventory)
        elif choice == "4":
            delete_product(inventory)
        elif choice == "5":
            inventory.display()
            print()
        elif choice == "6":
            print("Exiting Inventory System...")
            break
        else:
            print("Please enter a number from 1 to 6\n")


if __name__ == "__main__":
    main()
