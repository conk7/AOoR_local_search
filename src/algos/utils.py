from typing import List


def two_approx_solution(w: List[int], c: List[int], W: int):
    n = len(w)
    best_single_value = 0
    best_single_item = -1

    for i in range(n):
        if w[i] <= W and c[i] > best_single_value:
            best_single_value = c[i]
            best_single_item = i

    ratio_items = sorted(((c[i] / w[i], i) for i in range(n)), reverse=True)
    total_weight = 0
    total_value = 0
    chosen_items = []
    for _, i in ratio_items:
        if total_weight + w[i] <= W:
            total_weight += w[i]
            total_value += c[i]
            chosen_items.append(i)

    result_items = [0] * n
    if best_single_value >= total_value:
        if best_single_item != -1:
            result_items[best_single_item] = 1
        return result_items
    else:
        for i in chosen_items:
            result_items[i] = 1
        return result_items


__all__ = ["two_approx_solution"]
