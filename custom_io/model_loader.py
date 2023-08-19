import numpy as np
import pygame

from engine.GameObject import GameObject
from engine.Transform import Transform


def load_object(filename, tx_name, pos, rot, scale, sciplist=[]):
    object = GameObject()
    tx = pygame.surfarray.array3d(pygame.transform.flip(pygame.image.load(tx_name), False, True))

    with open(filename) as f:
        lines = f.readlines()

        points = []
        tris = []

        points_tx = []
        tris_tx = []

        for line in lines:
            if line.startswith('v '):
                sub_points = list(map(float, line[1:].strip().split(" ")))
                points.append(sub_points)
            elif line.startswith('vt'):
                points_tx.append([float(t.split('/')[0]) for t in line.split()[1:]])
            elif line.startswith('f'):
                triangle_str = line.split()[1:]
                triangle = [int(t.split('/')[0]) for t in triangle_str]
                tris.append(triangle)

                tris_tx.append(read_triangle_tx(triangle_str))

        main_tris = []
        main_tris_tx = []

        for idx, a in enumerate(tris):
            if idx not in sciplist:
                main_tris.extend(get_sub_triangles(a))
                main_tris_tx.extend(get_sub_triangles(tris_tx[idx]))

        object.tris = np.array(main_tris)
        object.points = np.array([update_point(a) for a in points])
        object.tx = tx
        object.calculate_tris_tx(main_tris_tx, points_tx)

        object.transform = Transform()
        object.transform.pos = np.array([*pos, 0.])
        object.transform.rot = np.array([*rot, 0.])
        object.transform.scale = np.array([*scale, 0.])

        return object


def read_triangle_tx(triangle_str):
    t_tx = []

    for t in triangle_str:
        temp = t.split('/')

        try:
            if len(temp) > 1:
                value = int(temp[1])
                t_tx.append(value)
            else:
                t_tx.append(0)
        except ValueError:
            t_tx.append(0)

    return t_tx


def get_sub_triangles(triangle):
    t_list = []

    t_list.append([
        triangle[0] - 1,
        triangle[1] - 1,
        triangle[2] - 1,
    ])

    num_points = len(triangle)
    left = num_points - 3

    for b in range(left):
        last = num_points - b
        if last == num_points: last = 0
        prelast = num_points - b - 1

        t_list.append([
            triangle[last] - 1,
            triangle[2] - 1,
            triangle[prelast] - 1,
        ])

    return t_list


def update_point(point):
    return [
        point[0],
        point[1],
        point[2],
        1.0
    ]
