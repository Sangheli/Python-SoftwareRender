import numpy as np

from engine.Transform import Transform


class GameObject:
    points = np.array([
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 0.0, 1.0, 1.0],
        [0.0, 1.0, 1.0, 1.0],
        [0.0, 0.0, 1.0, 1.0]
    ])

    tris = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [3, 2, 4],
        [3, 4, 5],
        [5, 4, 6],
        [5, 6, 7],
        [7, 6, 1],
        [7, 1, 0],
        [1, 6, 4],
        [1, 4, 2],
        [5, 7, 0],
        [5, 0, 3],
    ])

    tx = []
    tx_shift = [0, 0]

    def __init__(self):
        self.transform = Transform()

    def shift_center(self, vec4D):
        temp_points = self.points
        temp_points = np.array([self.shift_point(a, vec4D) for a in temp_points])
        self.points = temp_points

    @staticmethod
    def shift_point(point, shift):
        return [
            point[0] + shift[0],
            point[1] + shift[1],
            point[2] + shift[2],
            point[3],
        ]

    def calculate_tris_tx(self, tris_tx, points_tx):
        self.tris_tx = np.zeros(shape=(len(self.tris), 3, 2))

        for row, t_tx in enumerate(tris_tx):
            for sub_row, t_tx_index in enumerate(t_tx):
                self.tris_tx[row][sub_row][0] = points_tx[t_tx_index][0]
                self.tris_tx[row][sub_row][1] = points_tx[t_tx_index][1]
