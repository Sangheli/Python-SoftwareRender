# https://www.codecamp.ru/blog/moving-average-python/
# moving_avg fps

import numpy as np
import pygame

from settings import constant, color, settings

fps_arr = []


def draw_grid(pyscreen):
    pygame.draw.line(pyscreen, color.black, (settings.h_w, 0), (settings.h_w, settings.height), 2)
    pygame.draw.line(pyscreen, color.black, (0, settings.h_h), (settings.width, settings.h_h), 2)


def print_caption(clock, tris_len):
    fps = clock.get_fps()
    min = 0
    max = 0
    avg = 0

    if fps > constant.EPS:
        start = 100 if len(fps_arr) > 100 else 0
        fps_arr.append(fps)
        min = np.min(fps_arr[start:])
        max = np.max(fps_arr[start:])
        avg = np.average(fps_arr[start:])

    pygame.display.set_caption(f'[fps] {fps:.0f} ' +
                               f'[avg] {avg:.0f} ' +
                               f'[min] {min:.0f} ' +
                               f'[max] {max:.0f} ' +
                               f'[tris] {tris_len}'
                               )
