import pygame
from pygame.locals import *


def set_window(width, height, flags, vsync):
    return pygame.display.set_mode((width, height), flags, vsync)


def set_caption(caption):
    return pygame.display.set_caption(caption)


def create_clock():
    return pygame.time.Clock()


def events():
    return pygame.event.get()


def display_update():
    pygame.display.update()


def get_pressed_key():
    return pygame.key.get_pressed()


def get_mouse_pos():
    return pygame.mouse.get_pos()


def get_mouse_pressed():
    return pygame.mouse.get_pressed()


def load_image(path):
    return pygame.image.load(path)


def set_surface(width, height):
    return pygame.Surface((width, height))


# Input
class Input:
    def __init__(self, events, key_pressed, mouse_pos, mouse_pressed):
        self.events = events
        self.key_pressed = key_pressed
        self.mouse_pos = mouse_pos
        self.mouse_pressed = mouse_pressed

    """KEYBOARD"""

    def get_key_down(self, key):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                return event.key == key

    def get_key_up(self, key):
        for event in self.events:
            if event.type == pygame.KEYUP:
                return event.key == key

    def get_key(self, key):
        return bool(self.key_pressed[key])

    """MOUSE"""

    def get_mouse_button(self, mouse_button):
        return bool(self.mouse_pressed[mouse_button])

    def get_mouse_button_down(self, mouse_button):
        return any(
            (event.type == pygame.MOUSEBUTTONDOWN and self.mouse_pressed[mouse_button])
            for event in self.events
        )

    def get_mouse_button_up(self, mouse_button):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONUP:
                return bool(self.mouse_pressed[mouse_button])
        return False


# GameObject
class GameObject:
    def __init__(self, x, y, width, height, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprite = sprite

    def draw_object(self, surface):
        surface.blit(self.sprite, self.rect)
