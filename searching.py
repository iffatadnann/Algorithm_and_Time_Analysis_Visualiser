# searching.py
# Generator-style and pure implementations for searching algorithms

import math
import random

# Generator-style: yields ('compare', i, None), ('found', i), ('done',)
def linear_search_gen(arr, target):
    comparisons = 0
    for i, v in enumerate(arr):
        comparisons += 1
        yield ('compare', i, None)
        if v == target:
            yield ('found', i, comparisons)
            yield ('done',)
            return
    yield ('done', comparisons)

def binary_search_gen(arr, target):
    comparsions = 0
    left, right = 0, len(arr)-1
    while left <= right:
        comparsions += 1
        mid = (left + right) // 2
        yield ('compare', mid, None)
        if arr[mid] == target:
            yield ('found', mid, comparsions); yield ('done', comparsions); return
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    yield ('done', comparsions)

def jump_search_gen(arr, target):
    comparisons = 0
    n = len(arr)
    if n == 0:
        yield ('done', comparisons)
        return
#to find the number of steps to jump to the correct block
    step = int(math.sqrt(n))
    prev = 0

    # Jump through the array in blocks
    while prev < n:
        next_idx = min(prev + step, n) - 1
        comparisons += 1
        yield ('compare', next_idx, None, comparisons)

        # If we passed or reached a value >= target, start linear search
        if arr[next_idx] >= target:
            for i in range(prev, next_idx + 1):
                comparisons += 1
                yield ('compare', i, None, comparisons)
                if arr[i] == target:
                    yield ('found', i, comparisons)
                    yield ('done', comparisons)
                    return
            yield ('done', comparisons)
            return

        prev += step

    # If not found
    yield ('done', comparisons)


# Pure functions for timing (non-visual)
def linear_search(arr, target):
    for i, v in enumerate(arr):
        if v == target:
            return i
    return -1

def binary_search(arr, target):
    l, r = 0, len(arr)-1
    while l <= r:
        m = (l + r) // 2
        if arr[m] == target: return m
        if arr[m] < target: l = m+1
        else: r = m-1
    return -1

def jump_search(arr, target):
    n = len(arr)
    step = int(math.sqrt(n)) if n>0 else 1
    prev = 0
    while prev < n:
        next_idx = min(n-1, prev + step - 1)
        if arr[next_idx] >= target:
            for i in range(prev, next_idx+1):
                if arr[i] == target:
                    return i
            return -1
        prev += step
    return -1

# helper
def random_sorted_array(n, low=1, high=1000000):
    import random
    a = [random.randint(low, high) for _ in range(n)]
    a.sort()
    return a
