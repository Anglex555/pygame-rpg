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
        super().__init__(x, y, 240, 280, "oak.png")
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 3, y + self.height / 6 * 4, self.width / 3, self.height / 20)

class Spruce(Tree):
    def __init__(self, x, y):
        super().__init__(x, y, 160, 240, "spruce.png")
        self.rect = pygame.Rect(x - 50, y + 100, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + self.width / 3, y + self.height / 5 * 3, self.width / 3, self.height / 20)
