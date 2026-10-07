"""Compare search speed: HashTable (linear probing) vs one-dimensional array"""
import random
import time
from datetime import date

from hash_table import HashTable
from product import Product

REPEATS = 200 # How many times each search is repeated and averaged
RANDOM_SEED = 42  # Fixed seed so every run uses the same test data

def is_prime(number):
    """Return True if number is a prime number"""
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def next_prime(number):
    """Return the smallest prime that is >= number"""
    while not is_prime(number):
        number += 1
    return number


def linear_search(products, product_id):
    """Check each product in the array, in order, until the ID matches"""
    for product in products:
        if product.product_id == product_id:
            return product
    return None


def average_time_ns(search, repeats=REPEATS):
    """Run search() many times and return the average time in nanoseconds"""
    start = time.perf_counter_ns()
    for _ in range(repeats):
        search()
    end = time.perf_counter_ns()
    return (end - start) / repeats


def build_test_data(size):
    """Create size products and put the SAME products into a HashTable and an array"""
    random.seed(RANDOM_SEED)
    ids = random.sample(range(1, size * 10), size)

    array = []
    table = HashTable(next_prime(size * 2))
    for product_id in ids:
        product = Product(product_id, f"Medicine {product_id}", "9.90", 50,
                          "Test", date(2030, 1, 1))
        array.append(product)
        table.insert(product_id, product)
    return table, array


if __name__ == "__main__":
    table, array = build_test_data(1000)
    print("Array length:", len(array))
    print("Table size:", len(table), "| Capacity:", table.capacity(),
          "| Load factor:", round(table.load_factor(), 2))
    print("First ID in array:", array[0].product_id)
    print("Same objects in both:",
          all(table.search(p.product_id) is p for p in array))