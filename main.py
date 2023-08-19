# https://github.com/Josephbakulikira/3D-perspective-projection-with-python-
import os

import numpy as np
import pygame
from pygame import surfarray

from engine import screen
from engine.camera import camera_input, camera
from scenes import scene_quake as SCENE
from settings import settings

os.environ["SDL_VIDEO_CENTERED"] = '1'
run = True
pygame.init()
pyscreen = pygame.display.set_mode((settings.width, settings.height), pygame.SCALED)
clock = pygame.time.Clock()
fps = 600
delta_time = 0
scene = SCENE
light_pos = np.array([-15.5, 10., -9., 0.])

d_campos = np.array([0., 0., 0., 0.])
d_camrot = np.array([0., 0., 0., 0.])
cam_moving_speed = 900
cam_rot_speed = 4

camera.transform.pos = scene.campos
camera.transform.rot = scene.camrot

def draw(light_pos, d_campos, d_camrot):
    camera.clear()
    camera.transform.update_transform(d_campos * cam_moving_speed, d_camrot * cam_rot_speed)
    for idx, obj in enumerate(scene.object_list): camera.draw_object(obj, light_pos)

    if not settings.only_z_buffer:
        color_buffer, tris_len = camera.get_data(scene)
        surfarray.blit_array(pyscreen, color_buffer)
    else:
        zbuffer_scr, tris_len = camera.get_z_buffer()
        surfarray.blit_array(pyscreen, zbuffer_scr)

    pygame.display.update()
    screen.print_caption(clock, tris_len)


while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        dx, dy, dz = camera_input.scan_control_move(delta_time)
        d_campos[0] = dx
        d_campos[1] = dy
        d_campos[2] = dz

        drx, dry = camera_input.scan_control_rotate(delta_time)
        d_camrot[0] = drx
        d_camrot[1] = dry

    scene.update(delta_time)
    draw(light_pos, d_campos, d_camrot)
    delta_time = clock.get_time() / 1000

pygame.quit()
