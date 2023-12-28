import pygame
import sys
import os

class Item:
    def __init__(self, x, y, width, height, name, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)