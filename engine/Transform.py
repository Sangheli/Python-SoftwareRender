import numpy as np

from math_op import matrix


class Transform:
    def __init__(self):
        self.pos = np.array([0., 0., 0., 0.])
        self.rot = np.array([0., 0., 0., 0.])  # anglePitch, angleYaw, angleRoll
        self.scale = np.array([1., 1., 1., 0.])

    def update_transform(self, dpos, drot):
        self.rot += drot
        self.move(dpos)


    def model_matrix(self):
        translation_matrix = matrix.get_translation_matrix(self.pos)
        rot_matrix = matrix.get_rot_matrix(self.rot)
        scale_matrix = matrix.get_scale_matrix(self.scale)
        return rot_matrix @ scale_matrix @ translation_matrix


    def move_absolute(self, shift):
        self.pos += shift


    def move(self,dpos):
        self.pos += dpos @ matrix.get_rot_matrix(self.rot)
        

    def add_rot_absolute(self, shift):
        self.rot += shift
