import pygame
from pygame.locals import *
import engine
import time
import os

pygame.init()

# Clock
clock = engine.create_clock()

# Window
win = engine.set_window(1280, 736, pygame.VIDEORESIZE, 1)


# Caption
caption = engine.set_caption("Snake Game!")

# Variables"
FPS = 60
game = True

gravity = 0.2

last_time = time.time()


# Sprites
playerSprite = engine.load_image(os.path.join("data", "sprite", "player.png"))
block0 = engine.load_image("./data/sprite/block0.png")
block1 = engine.load_image("./data/sprite/block1.png")
block2 = engine.load_image("./data/sprite/block2.png")

sprites = {
    "playerSprite": playerSprite,
    "block0": block0,
    "block1": block1,
    "block2": block2,
}

# Player
class Player:
    def __init__(self):
        self.game_object = engine.GameObject(64, 500, 32, 32, playerSprite)
        self.run_speed = 3
        self.max_speed = 3
        self.jump_speed = 5
        self.velocity_y = 0
        self.max_speed_x = 3
        self.dx = 0
        self.jump = 1
        self.selected_level = 1

    def teleport(self, x, y):
        self.velocity_y = 0
        self.dx = 0
        self.game_object.rect.x = x
        self.game_object.rect.y = y

    def update(self, surface, ground, input, selected_level):
        self.dx = 0

        # MOVEMENT
        if input.GetKey(K_a) and abs(self.dx) <= self.max_speed_x:
            self.dx -= self.run_speed
        if input.GetKey(K_d) and abs(self.dx) <= self.max_speed_x:
            self.dx += self.run_speed

        # JUMP
        if input.GetKeyDown(K_w) and self.jump > 0:
            self.velocity_y = -self.jump_speed
            self.jump -= 1

        # DETECT RECTS
        detect_ground = pygame.Rect(
            self.game_object.rect.x,
            self.game_object.rect.y + 4,
            self.game_object.width,
            self.game_object.height,
        )
        detect_ceiling = pygame.Rect(
            self.game_object.rect.x,
            self.game_object.rect.y - 4,
            self.game_object.width,
            self.game_object.height,
        )
        detect_sides = pygame.Rect(
            self.game_object.rect.x + self.dx,
            self.game_object.rect.y,
            self.game_object.width,
            self.game_object.height,
        )

        # GRAVITY
        self.velocity_y += gravity
        self.velocity_y = min(self.velocity_y, 10)
        self.game_object.rect.y += self.velocity_y

        for i in ground["blocks"]:
            """DETECT X"""
            if i.rect.colliderect(detect_sides):
                self.dx = 0

            """ DETECT Y """
            # DETEC GROUND
            if i.rect.colliderect(detect_ground):
                # DETECT LAVA
                if i.type == "block1":
                    self.teleport(64, 500)
                # DETECT FINISH
                if i.type == "block2" and selected_level < 3:
                    self.selected_level += 1
                    self.teleport(64, 500)

                if self.velocity_y > 0:
                    self.game_object.rect.y = i.rect.top - self.game_object.height
                    self.jump = 1
                    self.velocity_y = 0
            # DETECT CEILING
            if i.rect.colliderect(detect_ceiling) and self.velocity_y < 0:
                self.game_object.rect.y = i.rect.top + self.game_object.height
                self.velocity_y = 0

        # UPDATE X
        self.game_object.rect.x += self.dx

        # DRAW OBJECT
        self.game_object.draw_object(surface)


player = Player()

# BLOCK
class Block:
    def __init__(self, x, y, sprite, type):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.type = type  # "block0" : "NORMAL", "block1" : "LAVA", "block2" : "FINISH"
        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

    def draw_block(self, surface):
        surface.blit(self.sprite, self.rect)


# ENVIROMENT
def load_level(level):
    with open(f"./data/world/level{level}.txt", "r") as f:
        blocks = []
        for line in f.readlines():
            if line:
                x, y, type_block = line.split()
                blocks.append(Block(x, y, sprites[type_block], type_block))
        return {"blocks": blocks}


previousLevel = player.selected_level - 1
selectedLevel = player.selected_level
ground = load_level(selectedLevel)  # LOAD LEVEL

# Main Loop
while not Input.get_key_down(K_ESCAPE) and all(
    event.type != pygame.QUIT for event in Input.events
):

    win.fill((50, 50, 50))

    # LEVEL
    selectedLevel = player.selected_level
    if selectedLevel - previousLevel == 2:
        print(selectedLevel)
        ground = load_level(selectedLevel)
        previousLevel = selectedLevel - 1

    # INPUT
    Input = engine.Input(
        engine.events(),
        engine.get_pressed_key(),
        engine.get_mouse_pos(),
        engine.get_mouse_pressed(),
    )

    # PLAYER UPDATE
    player.update(win, ground, Input, selectedLevel)

    # DRAW WORLD
    for block in ground["blocks"]:
        block.DrawBlock(win)

    # DISPLAY UPDATE
    pygame.display.update()
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
