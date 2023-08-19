import numpy as np

from custom_io import model_loader
from engine import TextureCompiler

angle = 0
speed_angle = 3
speed_rot = 10
rot_shift = np.array([0, 0.05, 0])

object = model_loader.load_object(filename="_resources/teapot.obj", tx_name="texture/metal.png", pos=[0, 0, 5],
                                  rot=[0, 0, 0], scale=[1, 1, 1])

object_list = [object]
full_tx = TextureCompiler.compile_textures(object_list)

campos = np.array([0., 292.0449969, -600.94630171, 0.])
camrot = np.array([0.42, 0., 0., 0.])


def manipulate_objects(deltatime):
    global angle
    angle += speed_angle * deltatime
    object.transform.add_rot_absolute(rot_shift * speed_rot * deltatime)


def update(deltatime):
    manipulate_objects(deltatime)
