from typing import List
import random


def calculate_cost(
    F: List[List[int]],
    D: List[List[int]],
    perm: List[int],
) -> int:
    n = len(perm)
    return sum(F[i][j] * D[perm[i]][perm[j]] for i in range(n) for j in range(n))


def delta_cost_swap(
    F: List[List[int]],
    D: List[List[int]],
    perm: List[int],
    i: int,
    j: int,
) -> int:
    if i == j:
        return 0

    n = len(perm)
    pi, pj = perm[i], perm[j]
    delta = 0

    for k in range(n):
        if k == i or k == j:
            continue
        pk = perm[k]

        delta += (D[pj][pk] - D[pi][pk]) * F[i][k]
        delta += (D[pk][pj] - D[pk][pi]) * F[k][i]

        delta += (D[pi][pk] - D[pj][pk]) * F[j][k]
        delta += (D[pk][pi] - D[pk][pj]) * F[k][j]

    delta += (D[pj][pj] - D[pi][pi]) * F[i][i]
    delta += (D[pi][pi] - D[pj][pj]) * F[j][j]
    delta += (D[pj][pi] - D[pi][pj]) * F[i][j]
    delta += (D[pi][pj] - D[pj][pi]) * F[j][i]

    return delta


def best_improvement_local_search(
    F: List[List[int]],
    D: List[List[int]],
    perm: List[int] = None,
):
    if perm is None:
        perm = list(range(len(F)))
        random.shuffle(perm)

    n = len(perm)
    cost = calculate_cost(F, D, perm)

    improved = True
    while improved:
        improved = False
        best_delta = 0
        best_i, best_j = -1, -1

        for i in range(n):
            for j in range(i + 1, n):
                delta = delta_cost_swap(F, D, perm, i, j)
                if delta < best_delta:
                    best_delta = delta
                    best_i, best_j = i, j

        if best_delta < 0:
            perm[best_i], perm[best_j] = perm[best_j], perm[best_i]
            cost += best_delta
            improved = True

    return perm, cost
