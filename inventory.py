import pygame
import sys
import os

pygame.init()
width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 100
running = True

k = 1 if width == 1920 else 1.4055636896

cells = [(74 // k, 250 // k), (222 // k, 250 // k), (370 // k, 250 // k), (518 // k, 250 // k), (666 // k, 250 // k),
         (814 // k, 250 // k), (962 // k, 250 // k), (1110 // k, 250 // k), (74 // k, 399 // k),
         (222 // k, 399 // k), (370 // k, 399 // k), (518 // k, 399 // k), (666 // k, 399 // k), (814 // k, 399 // k),
         (962 // k, 399 // k), (1110 // k, 399 // k), (74 // k, 548 // k), (222 // k, 548 // k),
         (370 // k, 548 // k), (518 // k, 548 // k), (666 // k, 548 // k), (814 // k, 548 // k), (962 // k, 548 // k),
         (1110 // k, 548 // k), (74 // k, 697 // k), (222 // k, 697 // k), (370 // k, 697 // k),
         (518 // k, 697 // k), (666 // k, 697 // k), (814 // k, 697 // k), (962 // k, 697 // k), (1110 // k, 697 // k)]

artifact_cell1 = (1297 // k, 321 // k)
artifact_cell2 = (1688 // k, 321 // k)
helmet_cell = (1494 // k, 321 // k)
armor_cell = (1495 // k, 535 // k)
sword_cell = (1299 // k, 535 // k)

items_positions = {}


class Inventory(pygame.sprite.Sprite):
    image_inventory = pygame.image.load('pics/whole_inventory3.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Inventory.image_inventory
        self.rect = self.image.get_rect()
        self.rect.x = 60 // k
        self.rect.y = 241 // k


class InventoryItem(pygame.sprite.Sprite):

    def __init__(self, indx, img, img_path, inv_pos, *group):
        super().__init__(*group)
        self.indx = indx
        self.image = pygame.transform.scale(img, (136 // k, 136 // k))
        self.rect = self.image.get_rect()
        if inv_pos:
            self.rect.x = inv_pos[0]
            self.rect.y = inv_pos[1]
        else:
            self.rect.x = cells[indx][0]
            self.rect.y = cells[indx][1]
        self.image_path = img_path
        self.is_mouse_track = False
        self.is_holding = None
        self.cursor_pos = [0, 0]

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            if self.is_holding:
                x = args[0].pos[0] - self.cursor_pos[0]
                y = args[0].pos[1] - self.cursor_pos[1]
                self.rect.x, self.rect.y = x, y
            else:
                if self.rect.collidepoint(args[0].pos):
                    self.image.set_alpha(200)
                    self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(100)
            self.is_holding = True
            self.cursor_pos[0] = args[0].pos[0] - self.rect.x
            self.cursor_pos[1] = args[0].pos[1] - self.rect.y
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            is_in_cell = False
            for i in cells:
                if abs(i[0] - self.rect.x) <= 80 and abs(i[1] - self.rect.y) <= 80:
                    self.rect.x, self.rect.y = i[0], i[1]
                    is_in_cell = True
                    self.indx = cells.index(i)
            if not is_in_cell:
                self.rect.x, self.rect.y = cells[self.indx][0], cells[self.indx][1]
            self.image.set_alpha(200)
            self.is_holding = False
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            if not self.is_holding:
                self.is_mouse_track = False
                self.image.set_alpha(255)
