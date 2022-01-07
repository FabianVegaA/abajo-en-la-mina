import pygame
import math
import random
import time
from scripts.particle import Particle
import numpy as np
from scripts.constants import *
from scripts.images import *

import logging

pygame.font.init()

particles = []
entities = []


def load_map(map_name):
    blocks = []
    with open(map_name, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            stripped_line = stripped_line.split(" ")
            blocks.append(stripped_line)
        a_file.close()

    lights = []
    gold = []
    enemies = []
    for block in blocks:
        if block[2] == "block14":  # If the block is long grass
            lights.append([int(block[0]), int(block[1]) - 350])

        if block[2] == "block15":  # If the block is long grass
            enemies.append([int(block[0]), int(block[1]) - 350])

            blocks.remove(block)
        if block[2] == "block0":  # If the block is long grass
            gold.append([int(block[0]), int(block[1]) - 350])

            blocks.remove(block)

    return blocks, lights, gold, enemies


def load_font(font_name, font_size):
    return pygame.font.Font(font_name, font_size)


def get_text_rect(text):
    return text.get_rect()


def render_text(display, text, font, bold, color, position):
    text = font.render(text, bold, color)
    display.blit(text, position)


def render_button(display, text, font, bold, color, position, clicking):
    text = font.render(text, bold, color)
    text_rect = get_text_rect(text)
    text_rect.center = (
        position[0] + text_rect.width / 2,
        position[1] + text_rect.height / 2,
    )

    display.blit(text, position)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = (mouse_x, mouse_y)

    if text_rect.collidepoint(mouse_pos):
        pygame.draw.rect(display, color, text_rect, 1)


def calculate_delta_time(prev_time):
    now = time.time()
    dt = now - prev_time
    prev_time = now

    return dt, prev_time


def particle_burst():
    for _ in range(1):
        particles.append(
            Particle(
                random.randrange(0, 400),
                -15,
                random.randrange(-1, 1),
                -0.05,
                4,
                (163, 167, 194),
                1,
            )
        )


def handle_particles(display, scroll):
    for particle in particles:
        if particle.lifetime > 0:
            particle.draw(display, scroll)
        else:
            particles.remove(particle)


def render_shadows(display, scroll, shadow_size):
    for i in reversed(range(3)):
        pygame.draw.circle(
            display,
            (0, 0, 0, i * 50),
            (100 - scroll[0] + 16, 100 - scroll[1] + 16),
            (shadow_size + (i * 10)),
        )


cache = {}


def cache_wrapper(func):
    if not func in cache:
        cache[func] = {}

    def cached_func(*args):
        if args in cache[func]:
            return cache[func][args]
        value = func(*args)
        cache[func][args] = value
        return value

    return cached_func


def fill_displays(displays, colors):
    for index, display in enumerate(displays):
        display.fill(colors[index])


def animate(image_list, animation_index, time_to_show_image_on_screen):
    if animation_index + 1 >= len(image_list) * time_to_show_image_on_screen:
        animation_index = 0
    animation_index += 1

    return animation_index


@cache_wrapper  # Cache the font :D
def render_fps_font(font, fps):
    return font.render(fps, True, WHITE)


@cache_wrapper
def rotate(image, rotation):
    return pygame.transform.rotate(image, rotation)


def play_sound(path_to_sound):
    sound = pygame.mixer.Sound(path_to_sound)
    sound.play()


def render_tiles(display, scroll, tiles, player_pos, tile_index):
    tile_rects = []
    for title in tiles:
        tile_rects.append([int(title[0]), int(title[1]) - 350, 16, 16, title[2]])
        x = int(title[0]) - scroll[0]
        y = int(title[1]) - scroll[1] - 350
        dist = math.hypot(player_pos[0] - x, player_pos[1] - y)
        if dist < 100:
            try:
                display.blit(tile_index[title[2]], (x, y))
            except KeyError as e:
               logging.warning(e)

    return tile_rects


def render_grass(display, scroll, grass, dt, player):
    for img in grass:
        if (
            img[1] - int(img[0].get_width() / 2) - scroll[0] > -20
            and img[1] - int(img[0].get_width() / 2) - scroll[0] < 350
        ):
            if pygame.Rect(
                player.player_rect.x - scroll[0] - 8,
                player.player_rect.y - scroll[1] - 8,
                player.player_rect.width + 16,
                player.player_rect.height + 16,
            ).colliderect(
                pygame.Rect(
                    img[1] - int(img[0].get_width() / 2) - scroll[0] + 10,
                    img[2] - int(img[0].get_height() / 2) - scroll[1] + 10,
                    8,
                    16,
                )
            ):
                img_copy = pygame.transform.rotate(img[0], (np.sin(img[3])) * img[4])
            else:
                img[3] += dt
                img_copy = rotate(img[0], round((np.sin(img[3])) * 10, 5))

            display.blit(
                img_copy,
                (
                    img[1] - img[0].get_width() // 2 - scroll[0],
                    img[2] - img[0].get_height() // 2 - scroll[1],
                ),
            )


def ghost_effect(entity):
    entity.alpha -= 5


def jump_effect(entity):
    entity.alpha -= 20


def circle_surf(radius, color):
    surf = pygame.Surface((radius, radius))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


def flame_effect(display, entity, shadows, scroll, sine):
    if entity.radius > 1:
        entity.radius -= 0.04
    else:
        entities.remove(entity)

    pygame.draw.circle(
        shadows,
        (255, 140, 60, 100),
        (entity.x - scroll[0], entity.y - scroll[1]),
        (1.5 * entity.radius) + sine * 5,
    )


def render_button(display, text, font, bold, color, position, clicking, func, thing):
    text = font.render(text, bold, color)
    text_rect = get_text_rect(text)
    text_rect.height -= 10
    text_rect.center = (
        position[0] + text_rect.width / 2,
        position[1] + text_rect.height / 2,
    )

    display.blit(text, position)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = (mouse_x / 3, mouse_y / 3)

    if thing and text_rect.collidepoint(mouse_pos):
        pygame.draw.rect(
            display,
            color,
            (text_rect.x, text_rect.y + 10, text_rect.width, text_rect.height),
            1,
        )
        if clicking:
            func()
            clicking = False
