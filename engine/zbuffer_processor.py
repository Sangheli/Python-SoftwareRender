from numba import njit

from math_op import math_custom
from settings import constant


@njit(fastmath=True)
def process(display, z_buffer, texture_buffer, v0, v1, v2, index):
    min_x, max_x = math_custom.get_min_max(v0[0], v1[0], v2[0])
    min_y, max_y = math_custom.get_min_max(v0[1], v1[1], v2[1])
    min_z, max_z = math_custom.get_min_max_float(v0[2], v1[2], v2[2])

    v0mv1 = v0 - v1
    v1mv2 = v1 - v2
    v2mv0 = v2 - v0

    for y in range(min_y - 1, max_y + 1, 1):
        if y < 0 or y >= display[1]: continue

        for x in range(min_x - 1, max_x + 1, 1):
            if x < 0 or x >= display[0]: continue
            if min_z > z_buffer[x][y]: continue

            if calc_triangle_edge(v1, v0mv1, x, y) >= 0.0:
                if calc_triangle_edge(v2, v1mv2, x, y) >= 0.0:
                    if calc_triangle_edge(v0, v2mv0, x, y) >= 0.0:
                        new_z = calc_triangle_z(v0, v1, v2, x, y)
                        if new_z < z_buffer[x][y]:
                            z_buffer[x][y] = new_z
                            texture_buffer[x][y] = index


@njit(fastmath=True)
def calc_triangle_edge(v0, b, x, y):
    a0 = x - v0[0]
    a1 = y - v0[1]
    return a0 * b[1] - a1 * b[0]


@njit(fastmath=True)
def calc_triangle_z(p0, p1, p2, x, y):
    det = (p1[1] - p2[1]) * (p0[0] - p2[0]) + (p2[0] - p1[0]) * (p0[1] - p2[1])
    if det < constant.EPS: det = 0.001
    l0 = ((p1[1] - p2[1]) * (x - p2[0]) + (p2[0] - p1[0]) * (y - p2[1])) / det
    l1 = ((p2[1] - p0[1]) * (x - p2[0]) + (p0[0] - p2[0]) * (y - p2[1])) / det
    l2 = 1.0 - l0 - l1

    return l0 * p0[2] + l1 * p1[2] + l2 * p2[2]
