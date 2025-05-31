import random
from typing import List
from .best_improvement import best_improvement_local_search

NUM_ITERATIONS = 100


def perturbation(perm: List[int], n: int = 3):
    perm = perm[:]
    n = len(perm)
    for _ in range(n):
        i, j = random.sample(range(n), 2)
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def iterated_local_search(F: List[List[int]], D: List[List[int]]):
    current_perm = list(range(len(F)))
    random.shuffle(current_perm)
    current_perm, current_cost = best_improvement_local_search(F, D, perm=current_perm)

    best_perm = current_perm[:]
    best_cost = current_cost

    for _ in range(NUM_ITERATIONS):
        new_perm = perturbation(current_perm)
        new_perm, new_cost = best_improvement_local_search(F, D, perm=new_perm)
        if new_cost < current_cost:
            current_perm, current_cost = new_perm, new_cost
        if new_cost < best_cost:
            best_perm, best_cost = new_perm[:], new_cost

    return best_perm, best_cost
