import math

import numpy as np
from numba import njit

from settings import constant


@njit()
def calculate_triangle_dot_pos(target_pos, p1, p2, p3):
    t_norm = calculate_normal(p1, p2, p3)
    d_pos = target_pos - p1
    sqr_abs_value = sqr_abs(d_pos)
    d_pos_norm = normalized(d_pos, sqr_abs_value)
    return dot(t_norm, d_pos_norm)


@njit()
def calculate_normal(p1, p2, p3):
    v1 = p2 - p1
    v2 = p3 - p1
    cross_product = cross(v1, v2)

    sqr_abs_value = sqr_abs(cross_product)
    if sqr_abs_value > constant.EPS:
        return normalized(cross_product, sqr_abs_value)
    else:
        return constant.zeroVec3


@njit()
def normalized(vec, sqr_abs_value):
    abs_value = math.sqrt(sqr_abs_value)
    if abs_value > constant.EPS:
        return vec / abs_value
    else:
        return constant.zeroVec3


@njit()
def cross(vec1, vec2):
    v = np.array([
        vec1[1] * vec2[2] - vec2[1] * vec1[2],
        vec1[2] * vec2[0] - vec2[2] * vec1[0],
        vec1[0] * vec2[1] - vec2[0] * vec1[1]
    ])

    return v


@njit()
def sqr_abs(vec): return vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2


@njit()
def dot(vec1, vec2): return vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]
