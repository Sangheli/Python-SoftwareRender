from numba import njit


@njit()
def get_tx_coordinate(x, y, tx_size_0, tx_size_1, pre_texture_data, text_points):
    sorted_y = [int(pre_texture_data[0]), int(pre_texture_data[1]), int(pre_texture_data[2])]

    slope_1 = pre_texture_data[3]
    slope_2 = pre_texture_data[4]
    slope_3 = pre_texture_data[5]

    x_start = pre_texture_data[6]
    y_start = pre_texture_data[7]

    x_mid = pre_texture_data[8]
    y_mid = pre_texture_data[9]

    x_end = pre_texture_data[10]
    y_end = pre_texture_data[11]

    x1, uv_inter1 = get_part1(text_points, sorted_y, y,
                              y_start, y_mid, y_end,
                              x_start, x_mid, x_end,
                              slope_1, slope_2, slope_3)

    x2, uv_inter2 = get_part2(text_points, sorted_y, y,
                              y_start, y_mid, y_end,
                              x_start, x_mid, x_end,
                              slope_1, slope_2, slope_3)

    if x1 > x2:
        x1, x2 = x2, x1
        uv_inter1, uv_inter2 = uv_inter2, uv_inter1

    uv = uv_inter1 + (uv_inter2 - uv_inter1) * (x - x1) / (x2 - x1 + 1e-16)

    tex_x = int(uv[0] * tx_size_0)
    tex_y = int(uv[1] * tx_size_1)

    if tex_x < 0: tex_x = 0
    if tex_y < 0: tex_y = 0

    if tex_x >= tx_size_0: tex_x = tx_size_0 - 1
    if tex_y >= tx_size_1: tex_y = tx_size_1 - 1

    return tex_x, tex_y


@njit()
def get_sorted_y(proj_points):
    return proj_points[:, 1].argsort()


@njit()
def get_slope(x_start, x_mid, x_end, y_start, y_mid, y_end):
    slope_1 = (x_end - x_start) / (y_end - y_start + 1e-16)
    slope_2 = (x_mid - x_start) / (y_mid - y_start + 1e-16)
    slope_3 = (x_end - x_mid) / (y_end - y_mid + 1e-16)

    return slope_1, slope_2, slope_3


@njit()
def get_uv_inter1(text_points, sorted_y, y, y_start, y_end):
    return text_points[sorted_y[0]] + (text_points[sorted_y[2]] - text_points[sorted_y[0]]) * (y - y_start) / (
            y_end - y_start + 1e-16)


@njit()
def get_part1(text_points, sorted_y, y, y_start, y_mid, y_end, x_start, x_mid, x_end, slope_1, slope_2, slope_3):
    x1 = x_start + int((y - y_start) * slope_1)
    uv_inter1 = get_uv_inter1(text_points, sorted_y, y, y_start, y_end)
    return x1, uv_inter1


@njit()
def get_part2(text_points, sorted_y, y, y_start, y_mid, y_end, x_start, x_mid, x_end, slope_1, slope_2, slope_3):
    if y < y_mid:
        x2 = x_start + int((y - y_start) * slope_2)
        uv_inter2 = text_points[sorted_y[0]] + (text_points[sorted_y[1]] - text_points[sorted_y[0]]) * (y - y_start) / (
                y_mid - y_start + 1e-16)

    else:
        x2 = x_mid + int((y - y_mid) * slope_3)
        uv_inter2 = text_points[sorted_y[1]] + (text_points[sorted_y[2]] - text_points[sorted_y[1]]) * (y - y_mid) / (
                y_end - y_mid + 1e-16)

    return x2, uv_inter2
