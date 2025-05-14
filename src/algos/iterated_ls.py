import random
from typing import List
from .first_improvement_ls import first_improvement_local_search


def swap(perm: List[int], n: int = 2):
    perm = perm[:]
    n = len(perm)
    for _ in range(n):
        i, j = random.sample(range(n), 2)
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def iterated_local_search(F: List[List[int]], D: List[List[int]], iterations: int = 10):
    n = len(F)
    current_perm = list(range(n))
    random.shuffle(current_perm)

    current_perm, current_cost = first_improvement_local_search(F, D, perm=current_perm)
    best_perm = current_perm[:]
    best_cost = current_cost

    for _ in range(iterations):
        new_perm = swap(current_perm)
        new_perm, new_cost = first_improvement_local_search(F, D, perm=new_perm)
        if new_cost < best_cost:
            best_perm, best_cost = new_perm[:], new_cost
            current_perm, current_cost = new_perm, new_cost
        else:
            current_perm = new_perm

    return best_perm, best_cost
