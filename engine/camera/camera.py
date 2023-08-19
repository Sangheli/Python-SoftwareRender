import numba
import numpy as np
from numba import njit

from engine import zbuffer_processor, texture_processor
from engine.Transform import Transform
from math_op import matrix, vec3
from settings import settings


max_len = 0

z_buffer = np.zeros(shape=(settings.width, settings.height))
texture_buffer = np.ones(shape=(settings.width, settings.height), dtype=np.int32) * -1
color_buffer = np.zeros(shape=(settings.width, settings.height, 3))
tris = np.zeros(shape=(settings.max_tris_len, 3, 3))
text_points = np.zeros(shape=(settings.max_tris_len, 3, 2))
tris_color = np.zeros(shape=(settings.max_tris_len, 3))
lights = np.zeros(shape=(settings.max_tris_len))
pre_texture_data = np.zeros(shape=(settings.max_tris_len, 12))
texture_params = np.zeros(shape=(settings.max_tris_len, 4), dtype=np.int32)

PROJECTION_MATRIX = matrix.get_projection_matrix(settings.width, settings.height)
SCREEN_MATRIX = matrix.get_screen_matrix(settings.width, settings.height)

transform = Transform()


def clear():
    global max_len, z_buffer, color_buffer, texture_buffer
    max_len = 0
    z_buffer.fill(1000)
    texture_buffer.fill(-1)


def get_data(scene):
    calc_z_buffer(max_len, tris, z_buffer, texture_buffer)

    draw_color_buffer(color_buffer,
                      texture_buffer,
                      texture_params,
                      pre_texture_data,
                      text_points,
                      scene.full_tx,
                      lights)

    return color_buffer, max_len


def get_z_buffer():
    calc_z_buffer(max_len, tris, z_buffer, texture_buffer)
    return z_buffer, max_len


@njit(parallel=True)
def draw_color_buffer(color_buffer, texture_buffer, texture_params, pre_texture_data, text_points, tx, lights):
    for x in numba.prange(settings.width):
        for y in numba.prange(settings.height):
            index = texture_buffer[x][y]

            if index < 0:
                draw_back(color_buffer[x][y], 230)
                continue

            if settings.interlace and (x % 2 != 0 or y % 2 != 0):
                draw_back(color_buffer[x][y], 20)
                continue

            if settings.only_lighting:
                color_buffer[x][y][0] = lights[index] * 255
                color_buffer[x][y][1] = lights[index] * 255
                color_buffer[x][y][2] = lights[index] * 255
            else:
                t_x, t_y = texture_processor.get_tx_coordinate(x, y,
                                                               texture_params[index][0], texture_params[index][1],
                                                               pre_texture_data[index],
                                                               text_points[index])

                write_cb(color_buffer[x][y], tx, lights[index], t_x, t_y, texture_params[index])


@njit()
def write_cb(color_buffer, tx, light, t_x, t_y, shift):
    color_buffer[0] = tx[t_x + shift[2]][t_y + shift[3]][0] * light
    color_buffer[1] = tx[t_x + shift[2]][t_y + shift[3]][1] * light
    color_buffer[2] = tx[t_x + shift[2]][t_y + shift[3]][2] * light


@njit()
def draw_back(color_buffer, value):
    color_buffer[0] = value
    color_buffer[1] = value
    color_buffer[2] = value


@njit()
def calc_z_buffer(max, tris, z_buffer, texture_buffer):
    display = (settings.width, settings.height)
    for i in range(max):
        if not any_func(tris[i], settings.h_w, settings.h_h):
            zbuffer_processor.process(display,
                                      z_buffer,
                                      texture_buffer,
                                      tris[i][0],
                                      tris[i][1],
                                      tris[i][2],
                                      i
                                      )


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


def draw_object(object, light_pos):
    global max_len

    points = object.points @ object.transform.model_matrix()

    screen_projected = points @ get_camera_matrix() @ PROJECTION_MATRIX
    screen_projected /= screen_projected[:, -1].reshape(-1, 1)
    screen_projected[(screen_projected > 2) | (screen_projected < -2)] = 0  # fix tris zero calc
    screen_projected = screen_projected @ SCREEN_MATRIX

    dots = get_dots_arr(object.tris, points, transform.pos)
    get_tris_arr(tris, dots, object.tris, screen_projected, max_len)

    light_dots = get_dots_arr(object.tris, points, light_pos)
    get_lights_arr(lights, dots, light_dots, max_len)

    tx_size_0 = len(object.tx)
    tx_size_1 = len(object.tx[0])
    get_text_coord_arr(text_points, dots, object.tris_tx, max_len)
    fill_pretextured_data(pre_texture_data, tris, dots, max_len)
    get_texture_param(texture_params, dots, max_len, tx_size_0, tx_size_1, object.tx_shift[0], object.tx_shift[1])

    len_ = (dots >= 0).sum()
    max_len += len_


def get_camera_matrix():
    return matrix.get_translation_matrix(-transform.pos) @ matrix.get_rot_matrix(transform.rot).T


@njit()
def get_texture_param(texture_params, dots, shift, tx_size_0, tx_size_1, shift_x, shift_y):
    a = 0
    for idx, dot in enumerate(dots):
        if dot < 0: continue
        texture_params[a + shift][0] = tx_size_0
        texture_params[a + shift][1] = tx_size_1
        texture_params[a + shift][2] = shift_x
        texture_params[a + shift][3] = shift_y
        a += 1


@njit()
def fill_pretextured_data(pre_texture_data, tris, dots, shift):
    a = 0
    for i, dot in enumerate(dots):
        if dot < 0: continue

        sorted_y = tris[a + shift][:, 1].argsort()

        x_start, y_start, _ = tris[a + shift][sorted_y[0]]
        x_mid, y_mid, _ = tris[a + shift][sorted_y[1]]
        x_end, y_end, _ = tris[a + shift][sorted_y[2]]

        slope_1, slope_2, slope_3 = get_slope(x_start, x_mid, x_end, y_start, y_mid, y_end)

        pre_texture_data[a + shift][0] = sorted_y[0]
        pre_texture_data[a + shift][1] = sorted_y[1]
        pre_texture_data[a + shift][2] = sorted_y[2]

        pre_texture_data[a + shift][3] = slope_1
        pre_texture_data[a + shift][4] = slope_2
        pre_texture_data[a + shift][5] = slope_3

        pre_texture_data[a + shift][6] = x_start
        pre_texture_data[a + shift][7] = y_start

        pre_texture_data[a + shift][8] = x_mid
        pre_texture_data[a + shift][9] = y_mid

        pre_texture_data[a + shift][10] = x_end
        pre_texture_data[a + shift][11] = y_end

        a += 1


@njit()
def get_slope(x_start, x_mid, x_end, y_start, y_mid, y_end):
    slope_1 = (x_end - x_start) / (y_end - y_start + 1e-16)
    slope_2 = (x_mid - x_start) / (y_mid - y_start + 1e-16)
    slope_3 = (x_end - x_mid) / (y_end - y_mid + 1e-16)

    return slope_1, slope_2, slope_3


@njit()
def get_dots_arr(tris, points, target_pos):
    dots = np.zeros(shape=len(tris))

    for idx, t in enumerate(tris):
        d = vec3.calculate_triangle_dot_pos(target_pos, points[t[0]], points[t[1]], points[t[2]])
        dots[idx] = d

    return dots


@njit()
def get_tris_arr(tris, dots, t, p, shift):
    a = 0
    for i, dot in enumerate(dots):
        if dot < 0: continue
        to_triangle(tris[a + shift][0], p, t[i][0])
        to_triangle(tris[a + shift][1], p, t[i][1])
        to_triangle(tris[a + shift][2], p, t[i][2])
        a += 1


@njit()
def to_triangle(triangle, points, t):
    triangle[0] = points[t][0]
    triangle[1] = points[t][1]
    triangle[2] = points[t][2]


@njit()
def get_lights_arr(lights, dots, light_dots, shift):
    a = 0
    for i, dot in enumerate(dots):
        if dot < 0: continue
        lights[a + shift] = max(0.3, min(1, light_dots[i]))
        a += 1


def get_text_coord_arr(text_points, dots, tris_tx, shift):
    a = 0
    for i, dot in enumerate(dots):
        if dot < 0: continue

        text_points[a + shift][0][0] = tris_tx[i][0][0]
        text_points[a + shift][0][1] = tris_tx[i][0][1]
        text_points[a + shift][1][0] = tris_tx[i][1][0]
        text_points[a + shift][1][1] = tris_tx[i][1][1]
        text_points[a + shift][2][0] = tris_tx[i][2][0]
        text_points[a + shift][2][1] = tris_tx[i][2][1]

        a += 1
