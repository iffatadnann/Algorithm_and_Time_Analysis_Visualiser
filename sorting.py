

import math
import copy
import random


def bubble_sort_gen(arr):
    a = arr
    n = len(a)
    comparisons = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            yield ('compare', j, j+1)
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                yield ('swap', j, j+1)
    yield ('done', comparisons)

def insertion_sort_gen(arr):
    a = arr
    comparisons = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            yield ('compare', j, i)
            if a[j] > key:
                a[j+1] = a[j]
                yield ('overwrite', j+1, a[j+1])
                j -= 1
            else:
                break
        a[j+1] = key
        yield ('overwrite', j+1, key)
    yield ('done', comparisons)

def selection_sort_gen(arr):
    a = arr
    n = len(a)
    comparisons = 0
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            comparisons += 1
            yield ('compare', min_idx, j)
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            yield ('swap', i, min_idx)
    yield ('done', comparisons)

def merge_sort_gen(arr):
    a = arr
    comparisons = 0
    # recursive generator
    def merge_sort_range(left, right):
        nonlocal comparisons
        if right - left <= 1:
            return
        mid = (left + right) // 2
        yield from merge_sort_range(left, mid)
        yield from merge_sort_range(mid, right)
        i, j = left, mid
        temp = []
        while i < mid and j < right:
            comparisons += 1
            yield ('compare', i, j)
            if a[i] <= a[j]:
                temp.append(a[i]); i += 1
            else:
                temp.append(a[j]); j += 1
        while i < mid:
            temp.append(a[i]); i += 1
        while j < right:
            temp.append(a[j]); j += 1
        for k, val in enumerate(temp, start=left):
            a[k] = val
            yield ('overwrite', k, val)

    yield from merge_sort_range(0, len(a))
    yield ('done', comparisons)

def quick_sort_gen(arr):
    a = arr
    comparisons = 0

    def quick_rec(low, high):
        nonlocal comparisons
        if low < high:
            pivot = a[high]
            i = low - 1
            for j in range(low, high):
                comparisons += 1
                yield ('compare', j, high)
                if a[j] <= pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
                    yield ('swap', i, j)
            a[i+1], a[high] = a[high], a[i+1]
            yield ('swap', i+1, high)
            p = i+1
            yield from quick_rec(low, p-1)
            yield from quick_rec(p+1, high)

    yield from quick_rec(0, len(a)-1)
    yield ('done', comparisons)

def tim_sort_gen(arr, RUN=32):
    a = arr
    comparisons = 0
    # insertion on runs
    def insertion_on_range(left, right):
        nonlocal comparisons
        for i in range(left+1, right+1):
            key = a[i]; j = i-1
            while j >= left:
                comparisons += 1
                yield ('compare', j, i)
                if a[j] > key:
                    a[j+1] = a[j]; yield ('overwrite', j+1, a[j+1]); j -= 1
                else:
                    break
            a[j+1] = key; yield ('overwrite', j+1, key)

    def merge(left, mid, right):
        nonlocal comparisons
        L = a[left:mid+1]; R = a[mid+1:right+1]
        i = j = 0; k = left
        while i < len(L) and j < len(R):
            comparisons += 1
            yield ('compare', left + i, mid + 1 + j)
            if L[i] <= R[j]:
                a[k] = L[i]; i += 1
            else:
                a[k] = R[j]; j += 1
            yield ('overwrite', k, a[k]); k += 1
        while i < len(L):
            a[k] = L[i]; i += 1; yield ('overwrite', k, a[k]); k += 1
        while j < len(R):
            a[k] = R[j]; j += 1; yield ('overwrite', k, a[k]); k += 1

    n = len(a)
    for start in range(0, n, RUN):
        end = min(start + RUN - 1, n - 1)
        yield from insertion_on_range(start, end)
    size = RUN
    while size < n:
        for left in range(0, n, 2*size):
            mid = min(n-1, left + size - 1)
            right = min((left + 2*size - 1), n - 1)
            if mid < right:
                yield from merge(left, mid, right)
        size *= 2
    yield ('done', comparisons)

# --------------------
# Pure functions for timing (non-visual)
# These return sorted/result or index and are fast for profiling
# --------------------

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]; j = i-1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]; j -= 1
        a[j+1] = key
    return a

def selection_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def merge_sort(arr):
    a = arr.copy()
    if len(a) <= 1:
        return a
    mid = len(a)//2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:]); res.extend(right[j:])
    return res

def quick_sort(arr):
    a = arr.copy()
    if len(a) <= 1:
        return a
    pivot = a[len(a)//2]
    left = [x for x in a if x < pivot]
    middle = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def tim_sort(arr, RUN=32):
    a = arr.copy()
    n = len(a)
    for start in range(0, n, RUN):
        end = min(start+RUN, n)
        for i in range(start+1, end):
            key = a[i]; j = i-1
            while j >= start and a[j] > key:
                a[j+1] = a[j]; j -= 1
            a[j+1] = key
    size = RUN
    while size < n:
        for left in range(0, n, 2*size):
            mid = min(n-1, left+size-1)
            right = min((left+2*size-1), n-1)
            if mid < right:
                L = a[left:mid+1]; R = a[mid+1:right+1]
                i = j = 0; k = left
                while i < len(L) and j < len(R):
                    if L[i] <= R[j]:
                        a[k] = L[i]; i += 1
                    else:
                        a[k] = R[j]; j += 1
                    k += 1
                while i < len(L):
                    a[k] = L[i]; i += 1; k += 1
                while j < len(R):
                    a[k] = R[j]; j += 1; k += 1
        size *= 2
    return a

# small helper for random arrays if needed
def random_array(n, low=1, high=1000):
    return [random.randint(low, high) for _ in range(n)]
