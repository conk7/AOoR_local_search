import os
from pathlib import Path
import time
from typing import Callable, List
from tqdm import tqdm
from algos.best_improvement import calculate_cost

BENCHMARKS_PATH = Path().resolve() / "benchmarks"
ANSWERS_PATH = Path().resolve() / "report" / "answers"
N = 1


def measure_algo(algorithm: Callable, benchmarks_path: Path, N: int = 100):
    Ds = []
    Fs = []
    benchmarks = [p for p in list(benchmarks_path.glob("*")) if p.is_file()]
    for path in benchmarks:
        with open(path, "r") as f:
            n = int(f.readline().strip())
            D = []
            F = []

            for _ in range(n):
                line = f.readline().strip()
                D.append(list(map(int, line.split())))

            _ = f.readline()

            for _ in range(n):
                line = f.readline().strip()
                F.append(list(map(int, line.split())))

        Ds.append(D)
        Fs.append(F)

    avg_times = []
    total_perms = []
    total_costs = []
    for D, F in tqdm(zip(Ds, Fs), leave=False):
        total_time = 0

        for _ in tqdm(range(N), leave=False):
            start = time.time()
            perm, cost = algorithm(F=F, D=D)
            end = time.time()

            total_time += end - start

        total_perms.append(perm)
        total_costs.append(cost)

        avg_time = total_time / N
        avg_time *= 1000

        avg_times.append(avg_time)

    return (
        [p.stem for p in list(benchmarks_path.glob("*")) if p.is_file()],
        avg_times,
        total_perms,
        total_costs,
    )


def get_cost_from_file(benchmark: Path, answer: Path):
    with open(benchmark, "r") as f:
        n = int(f.readline().strip())
        D = []
        F = []

        for _ in range(n):
            line = f.readline().strip()
            D.append(list(map(int, line.split())))

        _ = f.readline()

        for _ in range(n):
            line = f.readline().strip()
            F.append(list(map(int, line.split())))

    with open(answer, "r") as f:
        line = f.readline().strip()
        perm = list(map(int, line.split()))
        perm = [x - 1 for x in perm]

    return calculate_cost(F, D, perm)


def print_results(
    algorithm: str,
    benchmarks: List[Path],
    avg_times: List[float],
    total_perms: List[List[int]],
    total_costs: List[int],
    answers_path: Path,
):
    print(f"\n\n{algorithm}")
    print(f"{'Benchmark':<15}{'Average time(ms)':<20}{'Distance':<15}")
    print("-" * 120)
    for benchmark, time_ms, perm, cost in zip(
        benchmarks, avg_times, total_perms, total_costs
    ):
        print(f"{benchmark:<15}{time_ms:<20.4f}{cost:<15}")
        file_path = answers_path / algorithm / (benchmark.__str__() + ".sol")
        file_path.touch()
        written_cost = get_cost_from_file(BENCHMARKS_PATH / benchmark, file_path)
        if cost < written_cost:
            with open(file_path, "w+") as file:
                perm = [x + 1 for x in perm]
                file.write(" ".join(map(str, perm)))
