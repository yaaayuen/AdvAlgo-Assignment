"""Fibonacci functions used in the concurrency experiment"""
import time

def fib(n):
    """Return the nth Fibonacci number using naive recursion 0(2^n)"""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def count_calls(n):
    """Return how many calls fib(n) makes, following the same recursion"""
    if n < 2:
        return 1
    return 1 + count_calls(n - 1) + count_calls(n - 2)


def fib_iterative(n):
    """Return the Fibonacci number with a loop 0(n), used to check answers"""
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


if __name__ == "__main__":
    for n in range(6):
        print(f"fib({n}) = {fib(n)}   calls = {count_calls(n)}")

    print("\nfib(40) checked with the fast loop:", fib_iterative(40))
    print("Calls made by fib(40) = 2 * fib(41) - 1 =", 2 * fib_iterative(41) - 1)

    start = time.perf_counter_ns()
    result = fib(30)
    end = time.perf_counter_ns()
    print(f"\nfib(30) = {result}, took {(end - start) / 1e9:.3f} seconds")