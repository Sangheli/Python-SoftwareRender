import numpy as np


def compile_textures(object_list):
    size_x = []
    size_y = []

    summ_x = 0
    summ_y = 0

    for obj in object_list:
        size_x.append(len(obj.tx))
        size_y.append(len(obj.tx[0]))

        summ_x += len(obj.tx)
        summ_y += len(obj.tx[0])

    max_y = np.max(size_y)
    max_x = np.max(size_x)

    if max_x >= max_y:
        mode = 0
        full_tx = np.zeros(shape=(summ_x, max_y, 3))
    else:
        mode = 1
        full_tx = np.zeros(shape=(max_x, summ_y, 3))

    shift_x = 0
    shift_y = 0

    for idx, obj in enumerate(object_list):
        obj.tx_shift = [shift_x, shift_y]
        for x in range(len(obj.tx)):
            for y in range(len(obj.tx[0])):
                full_tx[x + shift_x][y + shift_y][0] = obj.tx[x][y][0]
                full_tx[x + shift_x][y + shift_y][1] = obj.tx[x][y][1]
                full_tx[x + shift_x][y + shift_y][2] = obj.tx[x][y][2]

        if mode == 0:
            shift_x += len(obj.tx)
        else:
            shift_y += len(obj.tx[0])

    return full_tx
