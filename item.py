import pygame
import sys
import os

class Item:
    def __init__(self, x, y, width, height, name, image_path):
        self.x = x
        self.y = y
        self.image_path = image_path
        self.width = width
        self.height = height
        self.inventory_position = None
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        with open('unique_index.txt', mode='r') as file:
            self.unique_indx = int(file.readline().strip())
        with open('unique_index.txt', mode='w') as file:
            file.write(str(self.unique_indx + 1))
