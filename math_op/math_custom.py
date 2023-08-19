from numba import njit


@njit()
def get_min_max(a0, a1, a2):
    max = 0
    min = 10000000

    if a0 < min: min = a0
    if a0 > max: max = a0

    if a1 < min: min = a1
    if a1 > max: max = a1

    if a2 < min: min = a2
    if a2 > max: max = a2

    return int(min), int(max)


@njit()
def get_min_max_float(a0, a1, a2):
    max = 0
    min = 10000000

    if a0 < min: min = a0
    if a0 > max: max = a0

    if a1 < min: min = a1
    if a1 > max: max = a1

    if a2 < min: min = a2
    if a2 > max: max = a2

    return min, max


def get_min_max_2d(arr, axis):
    max = 0
    min = 10000000

    for a in arr:
        if a[axis] < min: min = a[axis]
        if a[axis] > max: max = a[axis]

    return min, max
