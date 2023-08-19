import math

import numpy as np

from custom_io import model_loader
from engine import TextureCompiler

angle = 0
speed_angle = 3
speed_rot = 70
rot_shift = np.array([0, 0.005, 0.005])
rot_shift2 = np.array([0.005, 0, 0])
rot_shift3 = np.array([0, 0, 0.005])

object1 = model_loader.load_object(filename="_resources/crate.obj", tx_name="_resources/crate.jpg", pos=[-1.5, 0, 50],
                                   rot=[0, 0, 0], scale=[0.5, 0.5, 0.5])
object2 = model_loader.load_object(filename="_resources/crate.obj", tx_name="_resources/crate.jpg", pos=[-1.5, 0, 50],
                                   rot=[0, 0, 0], scale=[0.5, 0.5, 0.5])
object3 = model_loader.load_object(filename="_resources/crate.obj", tx_name="_resources/crate.jpg", pos=[-1.5, 0, 50],
                                   rot=[0, 0, 0], scale=[0.5, 0.5, 0.5])

object_list = [object1, object2, object3]
full_tx = TextureCompiler.compile_textures(object_list)

campos = np.array([0., 292.0449969, -600.94630171, 0.])
camrot = np.array([0.42, 0., 0., 0.])


def manipulate_objects(deltatime):
    global angle
    angle += speed_angle * deltatime

    object1.transform.pos = [-math.cos(angle / 2) * 1.5, math.sin(angle / 2), math.cos(angle / 2) * 3 + 7]
    object2.transform.pos = [-math.cos(angle / 2) * 2.5, math.sin(angle * 2 / 2) / 2, 5]
    object3.transform.pos = [-math.cos(angle / 2) * 2.5, math.sin(angle / 2), 4.5]

    object1.transform.add_rot_absolute(rot_shift * speed_rot * deltatime)
    object2.transform.add_rot_absolute(rot_shift2 * speed_rot * deltatime)
    object3.transform.add_rot_absolute(rot_shift3 * speed_rot * deltatime)


def update(deltatime):
    manipulate_objects(deltatime)
