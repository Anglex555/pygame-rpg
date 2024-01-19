import pygame
import os


class House:
    def __init__(self, x, y, width, height, image_filename):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("data", image_filename)), (width, height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)


class House1(House):
    def __init__(self, x, y):
        super().__init__(x, y, 600, 600, "house1.png")

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)


class House2(House):
    def __init__(self, x, y):
        super().__init__(x, y, 600, 600, "house2.png")

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)


class House3(House):
    def __init__(self, x, y):
        super().__init__(x, y, 890, 740, "house3.png")

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)


class House4(House):
    def __init__(self, x, y):
        super().__init__(x, y, 935, 725, "house4.png")

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)


class House5(House):
    def __init__(self, x, y):
        super().__init__(x, y, 890, 590, "house5.png")

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)


class House6(House):
    def __init__(self, x, y):
        super().__init__(x, y, 890, 575, "house6.png")

    def update_rect(self, x, y):
        self.rect = pygame.Rect(x + 80, y + 250, self.width - 160, self.height - 450)
