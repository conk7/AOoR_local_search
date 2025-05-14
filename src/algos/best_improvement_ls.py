from typing import List
import random


def calculate_cost(
    F: List[List[int]],
    D: List[List[int]],
    perm: List[int],
) -> int:
    n = len(perm)
    return sum(F[i][j] * D[perm[i]][perm[j]] for i in range(n) for j in range(n))


def first_improvement_local_search(
    F: List[List[int]],
    D: List[List[int]],
    perm: List[int] = None,
    reset_frequency: int = 5,
):
    if perm is None:
        perm = list(range(len(F)))
        random.shuffle(perm)

    n = len(perm)
    cost = calculate_cost(F, D, perm)
    do_not_look = [False] * n
    iteration = 0

    improved = True
    while improved:
        improved = False
        iteration += 1

        if iteration % reset_frequency == 0:
            do_not_look = [False] * n

        for i in range(n):
            if do_not_look[i]:
                continue
            for j in range(i + 1, n):
                if do_not_look[j]:
                    continue

                new_perm = perm[:]
                new_perm[i], new_perm[j] = new_perm[j], new_perm[i]
                new_cost = calculate_cost(F, D, new_perm)

                if new_cost < cost:
                    perm = new_perm
                    cost = new_cost
                    improved = True
                    break

            if improved:
                break
            else:
                do_not_look[i] = True

    return perm, cost
