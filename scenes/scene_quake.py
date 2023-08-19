import math

import numpy as np

from custom_io import model_loader
from engine import TextureCompiler
from math_op import axis

angle = 0
speed_angle = 3
speed_rot = 10
rot_shift = np.array([0, 0.05, 0, 0])

object1 = model_loader.load_object(filename="_resources/quake/ranger/ranger.obj",
                                   tx_name="_resources/quake/ranger/ranger.png",
                                   pos=[100, 0, 0], rot=[0, 0, 0], scale=[1, 1, 1])

object2 = model_loader.load_object(filename="_resources/quake/demon/demon.obj",
                                   tx_name="_resources/quake/demon/demon.png",
                                   pos=[-100, 0, 0], rot=[0, 0, 0], scale=[1, 1, 1])

object3 = model_loader.load_object(filename="_resources/quake/shambler/Shambler.obj",
                                   tx_name="_resources/quake/shambler/Shambler.png",
                                   pos=[0, 0, 100], rot=[0, 0, 0], scale=[1, 1, 1])

object_cube = model_loader.load_object(filename="_resources/crate.obj", tx_name="_resources/grey_floor.jpg",
                                       pos=[0, -23, 0],
                                       rot=[0, 0, 0], scale=[150, 1, 150], sciplist=[])

object_list = [object_cube, object1, object2, object3]
full_tx = TextureCompiler.compile_textures(object_list)

campos = np.array([0., 292.0449969, -600.94630171, 0.])
camrot = np.array([0.42, 0., 0., 0.])


def manipulate_objects(deltatime):
    global angle
    angle += speed_angle * deltatime
    object1.transform.add_rot_absolute(rot_shift * speed_rot * deltatime)
    object2.transform.add_rot_absolute(rot_shift * speed_rot * deltatime)
    object3.transform.add_rot_absolute(rot_shift * speed_rot * deltatime)

    object1.transform.move(axis.forward*math.sin(angle)*2)
    object2.transform.move(axis.up*math.sin(angle)*2)
    object3.transform.move(axis.forward*deltatime*20)


def update(deltatime):
    manipulate_objects(deltatime)
