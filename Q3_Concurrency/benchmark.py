"""Time Fibonacci(35), (38), and (40) with and without multithreading"""
import sys
import time
import threading

from fibonacci import fib

FIB_VALUES = [35, 38, 40] # One thread for each value

def timed_fib(n, results, index):
    """Run fib(n) and store (n, answer, start_ns, end_ns) in results[index]"""
    start = time.perf_counter_ns()
    answer = fib(n)
    end = time.perf_counter_ns()
    results[index] = (n, answer, start, end)


def run_threaded():
    """Run each fib in its own thread. Return the results and T in nanoseconds"""
    results = [None] * len(FIB_VALUES)
    threads = []
    for index, n in enumerate(FIB_VALUES):
        thread = threading.Thread(target=timed_fib, args=(n, results, index))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first_start = min(start for _, _, start, _ in results)
    last_end = max(end for _, _, _, end in results)
    return results, last_end - first_start


if __name__ == "__main__":
    print("Python", sys.version.split()[0], "| GIL enabled:", sys._is_gil_enabled())

    results, elapsed = run_threaded()
    first_start = min(start for _, _, start, _ in results)
    for n, answer, start, end in results:
        print(f"Fib({n}) = {answer:,}  started at +{(start - first_start) / 1e9:.3f} s, "
              f"finished at +{(end - first_start) / 1e9:.3f} s")
    print(f"T = {elapsed:,} ns ({elapsed / 1e9:.2f} s)")