"""Time Fibonacci(35), (38), and (40) with and without multithreading"""
import sys
import time
import threading

from fibonacci import fib

FIB_VALUES = [35, 38, 40] # One thread for each value
ROUNDS = 10 # How many times each experiment is repeated

def timed_fib(n, results, index):
    """Run fib(n) and store (n, answer, start_ns, end_ns) in results[index]"""
    start = time.perf_counter_ns()
    answer = fib(n)
    end = time.perf_counter_ns()
    results[index] = (n, answer, start, end)


def elapsed_ns(results):
    """T = end time of the task that finished last - start time to the task that started first"""
    first_start = min(start for _, _, start, _ in results)
    last_end = max(end for _, _, _, end in results)
    return last_end - first_start


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
    return results, elapsed_ns(results)


def run_sequential():
    """Run each fib one after another, w/o threads; Return the results and T in nanoseconds"""
    results = [None] * len(FIB_VALUES)
    for index, n in enumerate(FIB_VALUES):
        timed_fib(n, results, index)
    return results, elapsed_ns(results)


def print_timeline(results):
    """Show when each calculation started and finished, measured from the first start"""
    first_start = min(start for _, _, start, _ in results)
    for n, _, start, end in results:
        print(f" Fib({n}) started at +{(start - first_start) / 1e9:.3f} s, "
              f"finished at +{(end - first_start) / 1e9:.3f} s")


def run_rounds(title, runner, rounds=ROUNDS):
    """Repeat one experiment, print every round, and return the average"""
    print(f"\n=== Fibonacci Computation ({title}) ===")
    times = []
    for round_number in range(1, rounds + 1):
        results, elapsed = runner()
        times.append(elapsed)
        answers = ", ".join(f"Fib({n})={answer}" for n, answer, _, _ in results)
        print(f"Round {round_number:>2}: {answers} | T = {elapsed:,} ns")
        if round_number == 1:
            print_timeline(results)

    average = sum(times) / len(times)
    print(f"Average T ({title}) : {average:,.0f} ns")
    print(f"Fastest round: {min(times):,} ns | Slowest round: {max(times):,} ns")
    return average


def main():
    """Run both experiments and compare their average times"""
    print("Python", sys.version.split()[0], "| GIL enabled:", sys._is_gil_enabled())
    threaded = run_rounds("With Multithreading", run_threaded)
    sequential = run_rounds("Without Multithreading", run_sequential)

    change = (threaded - sequential) / sequential * 100
    direction = "increased" if change > 0 else "reduced"
    print(f"\nObservation: Multithreading {direction} the average completion time "
          f"by approximately {abs(change):.1f}%")


if __name__ == "__main__":
    main()
