import pygame
from pygame.locals import *
import engine
import os
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfile

pygame.init()

# Clock
clock = engine.create_clock()
FPS = 30
# Window
infoObject = pygame.display.Info()
win = engine.set_window(1600, 900, pygame.RESIZABLE, 1)
blockSurface = engine.set_surface(1280, 736)

# Sprites

block0 = engine.load_image(os.path.join("data", "sprite", "block0.png"))

block1 = engine.load_image(os.path.join("data", "sprite", "BottomCornerLeft.png"))
block2 = engine.load_image(os.path.join("data", "sprite", "BottomCornerRight.png"))
block3 = engine.load_image(os.path.join("data", "sprite", "Center.png"))
block4 = engine.load_image(os.path.join("data", "sprite", "MiddleBottom.png"))
block5 = engine.load_image(os.path.join("data", "sprite", "MiddleRowLeft.png"))
block6 = engine.load_image(os.path.join("data", "sprite", "MiddleRowRight.png"))
block7 = engine.load_image(os.path.join("data", "sprite", "TopCornerLeft.png"))
block8 = engine.load_image(os.path.join("data", "sprite", "TopCornerRight.png"))
block9 = engine.load_image(os.path.join("data", "sprite", "TopMiddle.png"))

block10 = engine.load_image(os.path.join("data", "sprite", "Connecter.png"))
block11 = engine.load_image(os.path.join("data", "sprite", "Connecter2.png"))
block12 = engine.load_image(os.path.join("data", "sprite", "Connecter3.png"))
block13 = engine.load_image(os.path.join("data", "sprite", "Connecter4.png"))

block14 = engine.load_image(os.path.join("data", "sprite", "torch.png"))

block15 = engine.load_image(os.path.join("data", "sprite", "Skeleton1.png"))

sprites = {
    "block0": block0,
    "block1": block1,
    "block2": block2,
    "block3": block3,
    "block4": block4,
    "block5": block5,
    "block6": block6,
    "block7": block7,
    "block8": block8,
    "block9": block9,
    "block10": block10,
    "block11": block11,
    "block12": block12,
    "block13": block13,
    "block14": block14,
    "block15": block15,
}

# SPRITE OPTION
class SpriteOption:
    def __init__(self, rect, sprite_name):
        self.rect = rect
        self.sprite_name = sprite_name

    def draw(self, surface):
        surface.blit(sprites[self.sprite_name], self.rect)


# BLOCK
class Block:
    def __init__(self, color, rect):
        self.rect = rect
        self.main_color = color
        self.color = color
        self.sprite = ""

    def draw(self, surface):
        if self.sprite == "":
            pygame.draw.rect(surface, (self.color), self.rect)
        else:
            surface.blit(sprites[self.sprite], self.rect)


# FUNCTIONS
def create_blocks():
    z = 0
    blocks = []
    for x in range(0, 1312, 16):
        if z == 0:
            z = 1
        elif z == 1:
            z = 0
        for y in range(0, 768, 16):
            rect = pygame.Rect(x, y, 16, 16)
            if z == 0:
                color = (40, 40, 40)
                z += 1
            else:
                color = (35, 35, 35)
                z = 0
            blocks.append(Block(color, rect))
    return blocks


def save_world(blocks):
    text = "".join(
        f"{i.rect.x} {i.rect.y} {i.sprite}\n" for i in blocks if i.sprite != ""
    )

    extensions = [("Text Document", "*.txt")]

    f = asksaveasfile(mode="w", defaultextension=".txt", filetypes=extensions)
    if f is None:
        return

    f.write(text)
    f.close()


def open_world():
    blocks = create_blocks()

    extensions = [("Text Document", "*.txt")]
    f = askopenfile(filetypes=extensions)
    if f is None:
        return blocks

    for line in f.readlines():
        if line:
            x, y, block_type = line.split()
            for block in blocks:
                if int(x) == block.rect.x and int(y) == block.rect.y:
                    block.sprite = block_type
    return blocks


# APPENDING BLOCKS
blocks = create_blocks()
drawedSprites = []

# CHANGE SPRITE
spriteOptions = []
block = 30
y = 200
for z in sprites.items():
    rect = pygame.Rect(block, y, 32, 32)
    option = SpriteOption(rect, z[0])

    spriteOptions.append(option)
    y += 40


# VARIABLES
game = True
selectedSprite = "block0"

font = pygame.font.Font("freesansbold.ttf", 14)
selectedSpriteRect = pygame.Rect(10, 96, 10, 10)

while not Input.get_key_down(K_ESCAPE) and all(
    event.type != pygame.QUIT for event in Input.events
):
    win.fill((50, 50, 50))
    blockSurface.fill((100, 100, 100))
    # INPUT
    Input = engine.Input(
        engine.events(),
        engine.get_pressed_key(),
        engine.get_mouse_pos(),
        engine.get_mouse_pressed(),
    )

    # OPEN
    openRect = pygame.Rect(200, 30, 90, 30)
    openTextRect = pygame.Rect(200, 37, 60, 30)
    openRectText = font.render("Open World", True, (0, 0, 0))
    pygame.draw.rect(win, (255, 255, 255), openRect)
    win.blit(openRectText, openTextRect)

    if openRect.collidepoint(pygame.mouse.get_pos()) and Input.get_mouse_button_down(0):
        blocks = open_world()

    # SAVE
    saveRect = pygame.Rect(100, 30, 90, 30)
    saveTextRect = pygame.Rect(100, 37, 60, 30)
    saveRectText = font.render("Save World", True, (0, 0, 0))
    pygame.draw.rect(win, (255, 255, 255), saveRect)
    win.blit(saveRectText, saveTextRect)

    if saveRect.collidepoint(pygame.mouse.get_pos()) and Input.get_mouse_button_down(0):
        blocks = save_world(blocks)

    # OPTION
    selectedSpriteText = font.render("Selected Sprite: ", True, (255, 255, 255))

    win.blit(selectedSpriteText, selectedSpriteRect)
    win.blit(
        sprites[selectedSprite],
        (selectedSpriteRect.x + 32, selectedSpriteRect.y + 32, 32, 32),
    )

    for block in spriteOptions:
        if block.rect.collidepoint(
            pygame.mouse.get_pos()
        ) and Input.get_mouse_button_down(0):
            selectedSprite = block.spriteName
            print(selectedSprite)
        block.Draw(win)

    # BLOCKS
    if blocks is None:
        blocks = create_blocks()

    for block in blocks:
        if block.rect.collidepoint(
            pygame.mouse.get_pos()[0] - 160, pygame.mouse.get_pos()[1] - 82
        ):
            block.color = (80, 80, 80)

            # DRAW BLOCK
            if Input.get_mouse_button(0):
                print("yes")
                block.sprite = selectedSprite
            # ERASE BLOCK
            if Input.get_mouse_button_down(2):
                block.sprite = ""
        else:
            block.color = block.mainColor

        block.Draw(blockSurface)

    if Input.get_key_down(K_r):
        for block in blocks:
            if block.sprite:
                print(block.rect)

    win.blit(blockSurface, (160, 82))
    clock.tick(FPS)
    pygame.display.update()
