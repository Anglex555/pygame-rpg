import pygame
import os

class Tree:
    def __init__(self, x, y, width, height, image_filename):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("data", image_filename)), (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def update_rect(self, x, y):
        self.rect.topleft = (x, y)

class Oak(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 320, 390, "oak.png")
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 3, y + self.height / 6 * 4, self.width / 3, self.height / 20)

class SmallOak(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 288, 336, "small_oak.png")
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 3, y + self.height / 6 * 4, self.width / 3, self.height / 20)

class Spruce(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 192, 288, "spruce.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 3, y + self.height / 5 * 3, self.width / 3, self.height / 20)

class Pine(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 250, 390, "pine.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 4, y + self.height / 6 * 4, self.width / 2, self.height / 20)

class SnowPine(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 250, 390, "snow_pine.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 4, y + self.height / 6 * 4, self.width / 2, self.height / 20)

class SwampOak(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 240, 408, "swamp_oak.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 4, y + self.height / 6 * 4, self.width / 2, self.height / 20)

class DecorativeTree(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 156, 228, "decorative_tree.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 4, y + self.height / 6 * 4, self.width / 2, self.height / 20)

class DarkTree(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 260, 355, "dark_tree.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 4, y + self.height / 6 * 4, self.width / 2, self.height / 20)

class DesertTree(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 236, 312, "desert_tree.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 4, y + self.height / 6 * 4, self.width / 2, self.height / 20)

class MagicTree(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 252, 312, "magic_tree.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 4, y + self.height / 6 * 4, self.width / 2, self.height / 20)

class TropicalTree(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 252, 312, "tropical_tree.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 4, y + self.height / 6 * 4, self.width / 2, self.height / 20)
