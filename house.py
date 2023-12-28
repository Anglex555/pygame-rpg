import pygame
import os

class House1:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("data", "house.png")), (width, height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)

class House2:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("data", "house2.png")), (width, height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)

