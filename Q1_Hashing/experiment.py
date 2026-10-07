"""Compare search speed: HashTable (linear probing) vs one-dimensional array"""
import os
import random
import time
from datetime import date

from hash_table import HashTable
from product import Product

REPEATS = 200  # How many times each search is repeated and averaged
RANDOM_SEED = 42  # Fixed seed so every run uses the same test data
SIZES = [100, 1000, 10000, 100000]  # Number of products in each test
GRAPH_CASE = "Last"  # Which case to draw on the graph
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
GRAPH_FILE = os.path.join(RESULTS_DIR, "search_times.png")


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


def run_experiment(size):
    """Time hash table and array searches for one data size"""
    table, array = build_test_data(size)
    cases = {
        "First": array[0].product_id,
        "Middle": array[size // 2].product_id,
        "Last": array[-1].product_id,
        "Not found": size * 10
    }
    results = []
    for case, product_id in cases.items():
        _, probes = table.locate(product_id)
        hash_ns = average_time_ns(lambda: table.locate(product_id))
        array_ns = average_time_ns(lambda: linear_search(array, product_id))
        results.append([case, probes, hash_ns, array_ns])
    return results


def print_results(size, results):
    """Print one size's results as a lined-up table"""
    print(f"\n=== {size:,} products ===")
    print(f"{'Case':<10} {'Probes':>6} {'Hash table (ns)':>16} {'Array (ns)':>14} {'Array / Hash':>13}")
    for case, probes, hash_ns, array_ns in results:
        print(f"{case:<10} {probes:>6} {hash_ns:>16,.0f} {array_ns:>14,.0f} {array_ns / hash_ns:>12.1f}x")


def main():
    """Run the experiment for every size and print the results"""
    print(f"Each search is repeated {REPEATS} times; times are averages")
    all_results = {}
    for size in SIZES:
        results = run_experiment(size)
        all_results[size] = results
        print_results(size, results)
    return all_results


def plot_results(all_results, case=GRAPH_CASE):
    """Draw hash table vs array search time for one case and save it as a PNG"""
    import matplotlib.pyplot as plt

    sizes = list(all_results)
    hash_times = []
    array_times = []
    for size in sizes:
        for row_case, _, hash_ns, array_ns in all_results[size]:
            if row_case == case:
                hash_times.append(hash_ns)
                array_times.append(array_ns)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sizes, array_times, color="#eb6834", marker="s", markersize=8,
            linewidth=2, label="Array (linear search)")
    ax.plot(sizes, hash_times, color="#2a78d6", marker="o", markersize=8,
            linewidth=2, label="Hash table (linear probing)")
    ax.annotate("Array", (sizes[-1], array_times[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", color="#0b0b0b")
    ax.annotate("Hash table", (sizes[-1], hash_times[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", color="#0b0b0b")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Number of products (log scale)")
    ax.set_ylabel("Average search time in ns (log scale)")
    ax.set_title(f"Search time vs number of products ({case} case)")
    ax.grid(True, which="major", color="#e4e3df", linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, loc="upper left")
    ax.set_xlim(right=sizes[-1] * 3)
    fig.tight_layout()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    fig.savefig(GRAPH_FILE, dpi=150)
    print(f"\nGraph saved to {GRAPH_FILE}")
    plt.show()


if __name__ == "__main__":
    plot_results(main())
