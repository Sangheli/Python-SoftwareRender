import pygame


def scan_control_move(deltatime):
    x = 0
    y = 0
    z = 0

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        x -= 0.5 * deltatime
    if key[pygame.K_d]:
        x += 0.5 * deltatime
    if key[pygame.K_w]:
        z += 0.5 * deltatime
    if key[pygame.K_s]:
        z -= 0.5 * deltatime
    if key[pygame.K_q]:
        y -= 0.5 * deltatime
    if key[pygame.K_e]:
        y += 0.5 * deltatime

    return x, y, z


def scan_control_rotate(deltatime):
    x = 0
    y = 0

    key = pygame.key.get_pressed()
    if key[pygame.K_j]:
        y -= 0.5 * deltatime
    if key[pygame.K_l]:
        y += 0.5 * deltatime
    if key[pygame.K_i]:
        x -= 0.5 * deltatime
    if key[pygame.K_k]:
        x += 0.5 * deltatime

    return x, y
