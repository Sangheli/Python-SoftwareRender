import numpy as np

from custom_io import model_loader
from engine import TextureCompiler

angle = 0
speed_angle = 0.5
speed_rot = 250
rot_shift2 = np.array([0, -0.005, 0])

object = model_loader.load_object(filename="_resources/crate.obj", tx_name="_resources/crate.jpg", pos=[0, 0, 2],
                                  rot=[0.78, 0, 0], scale=[0.5, 0.5, 0.5], sciplist=[])
object_list = [object]
full_tx = TextureCompiler.compile_textures(object_list)

campos = np.array([0., 292.0449969, -600.94630171, 0.])
camrot = np.array([0.42, 0., 0., 0.])


def manipulate_objects(deltatime):
    global angle
    angle += speed_angle * deltatime

    object.transform.add_rot_absolute(rot_shift2 * speed_rot * deltatime)


def update(deltatime):
    manipulate_objects(deltatime)
