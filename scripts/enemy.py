import pygame
import random
import math
from scripts.framework import *
from scripts.images import *


class Enemy:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.rect = None


class FlyingEnemy(Enemy):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.speed = random.randrange(1, 3)
        self.offset = [random.randrange(-50, 50), random.randrange(-50, 50)]
        self.bullet_cooldown = 0
        self.animation_count = 0

    def draw(self, display, scroll, player_rect):
        self.rect = pygame.Rect(self.x - scroll[0], self.y - scroll[1], 16, 16)
        self.enemy_vector = pygame.Vector2(self.rect.center)
        self.player_vector = pygame.Vector2(
            pygame.Rect(
                player_rect.x - scroll[0] + self.offset[0],
                player_rect.y - scroll[1] + self.offset[1],
                player_rect.width,
                player_rect.height,
            ).center
        )

        if self.player_vector != self.enemy_vector:
            towards = (self.player_vector - self.enemy_vector).normalize() / self.speed
        else:
            towards = pygame.Vector2(0, 0)
        self.dist = math.hypot(
            (player_rect.x - scroll[0]) - (self.x - scroll[0]),
            (player_rect.y - scroll[1]) - (self.y - scroll[1]),
        )

        if self.dist > 40 and self.dist < 150:
            self.x += towards[0]
            self.y += towards[1]

        self.animation_count = animate(skeleton_imgs, self.animation_count, 5)
        display.blit(
            skeleton_imgs[self.animation_count // 5],
            (self.x - scroll[0], self.y - scroll[1]),
        )


class FlyingDestoryer(Enemy):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.speed = random.randrange(1, 3)
        self.offset = [random.randrange(-50, 50), random.randrange(-50, 50)]
        self.bullet_cooldown = 0
        self.animation_count = 0
        self.width = 1

    def draw(self, display, scroll, player_rect):
        self.rect = pygame.Rect(self.x - scroll[0], self.y - scroll[1], 16, 16)
        self.enemy_vector = pygame.Vector2(self.rect.center)
        self.player_vector = pygame.Vector2(
            pygame.Rect(
                player_rect.x - scroll[0] + self.offset[0],
                player_rect.y - scroll[1] + self.offset[1],
                player_rect.width,
                player_rect.height,
            ).center
        )

        if self.player_vector != self.enemy_vector:

            towards = (self.player_vector - self.enemy_vector).normalize() / self.speed
        else:
            towards = pygame.Vector2(0, 0)
        dist = math.hypot(
            (player_rect.x - scroll[0]) - (self.x - scroll[0]),
            (player_rect.y - scroll[1]) - (self.y - scroll[1]),
        )

        if dist > 80:
            self.x += towards[0]
            self.y += towards[1]

        self.animation_count = animate(skeleton_imgs, self.animation_count, 5)
        display.blit(
            skeleton_imgs[self.animation_count // 5],
            (self.x - scroll[0], self.y - scroll[1]),
        )
