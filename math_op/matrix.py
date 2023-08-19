import math

import numpy as np


def get_projection_matrix(witdh, height):
    h_fov = math.pi / 3
    v_fov = h_fov * (height / witdh)

    NEAR = 0.1
    FAR = 100
    RIGHT = math.tan(h_fov / 2)
    LEFT = -RIGHT
    TOP = math.tan(v_fov / 2)
    BOTTOM = -TOP

    m00 = 2 / (RIGHT - LEFT)
    m11 = 2 / (TOP - BOTTOM)
    m22 = (FAR + NEAR) / (FAR - NEAR)
    m32 = -2 * NEAR * FAR / (FAR - NEAR)

    return np.array([
        [m00, 0, 0, 0],
        [0, m11, 0, 0],
        [0, 0, m22, 1],
        [0, 0, m32, 0]
    ])


def get_screen_matrix(witdh, height):
    half_w = witdh // 2
    half_h = height // 2

    return np.array([
        [half_w, 0, 0, 0],
        [0, -half_h, 0, 0],
        [0, 0, 1, 0],
        [half_w, half_h, 0, 1]
    ])


def get_rot_matrix(rot):
    return rot_x(rot[0]) @ rot_y(rot[1]) @ rot_z(rot[2])


def rot_x(angle):
    m_cos = math.cos(angle)
    m_sin = math.sin(angle)

    return np.array([
        [1, 0, 0, 0],
        [0, m_cos, m_sin, 0],
        [0, -m_sin, m_cos, 0],
        [0, 0, 0, 1]
    ])


def rot_y(angle):
    m_cos = math.cos(angle)
    m_sin = math.sin(angle)

    return np.array([
        [m_cos, 0, -m_sin, 0],
        [0, 1, 0, 0],
        [m_sin, 0, m_cos, 0],
        [0, 0, 0, 1]
    ])


def rot_z(angle):
    m_cos = math.cos(angle)
    m_sin = math.sin(angle)

    return np.array([
        [m_cos, m_sin, 0, 0],
        [-m_sin, m_cos, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def get_scale_matrix(scale):
    return np.array([
        [scale[0], 0, 0, 0],
        [0, scale[1], 0, 0],
        [0, 0, scale[2], 0],
        [0, 0, 0, 1]
    ])


def get_translation_matrix(v):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [v[0], v[1], v[2], 1]
    ])
