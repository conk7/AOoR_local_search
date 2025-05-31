from algos import (
    iterated_local_search,
    best_improvement_local_search,
)
from utils import measure_algo, print_results, BENCHMARKS_PATH, ANSWERS_PATH, N


def main():
    for algo in [best_improvement_local_search, iterated_local_search]:
        benchmarks, avg_times, total_perms, total_cost = measure_algo(
            algo, BENCHMARKS_PATH, N
        )
        print_results(
            algo.__name__,
            benchmarks,
            avg_times,
            total_perms,
            total_cost,
            ANSWERS_PATH,
        )


if __name__ == "__main__":
    main()
