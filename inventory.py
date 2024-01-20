import pygame
import sys
import os

pygame.init()
with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    width = int(file.read())
    height = (width // 16) * 9
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
shield_cell = (1690 // k, 535 // k)


items_positions = {}


class Inventory(pygame.sprite.Sprite):
    image_inventory = pygame.image.load('pics/whole_inventory4.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Inventory.image_inventory, (1800 // k, 597 // k))
        self.rect = self.image.get_rect()
        self.rect.x = 60 // k
        self.rect.y = 241 // k


class InventoryItem(pygame.sprite.Sprite):

    def __init__(self, indx, img, img_path, inv_pos, unique_indx, *group):
        super().__init__(*group)
        self.unique_indx = unique_indx
        self.indx = indx
        if inv_pos in (armor_cell, sword_cell, shield_cell):
            self.image = pygame.transform.scale(img, (136 // k, 272 // k))
        else:
            self.image = pygame.transform.scale(img, (136 // k, 136 // k))
        self.rect = self.image.get_rect()
        if inv_pos:
            self.rect.x = inv_pos[0]
            self.rect.y = inv_pos[1]
            items_positions[self] = (inv_pos[0], inv_pos[1])
        else:
            self.rect.x = cells[indx][0]
            self.rect.y = cells[indx][1]
            items_positions[self] = (cells[indx][0], cells[indx][1])
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
                if (abs(i[0] - self.rect.x) <= 80 and abs(i[1] - self.rect.y) <= 80
                        and i not in items_positions.values()):
                    self.image = pygame.transform.scale(self.image, (136 // k, 136 // k))
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = i[0], i[1]
                    is_in_cell = True
                    self.indx = cells.index(i)
                    items_positions[self] = (i[0], i[1])
            if not is_in_cell:
                if (abs(artifact_cell1[0] - self.rect.x) <= 80 and abs(artifact_cell1[1] - self.rect.y) <= 80
                        and artifact_cell1 not in items_positions.values()) and 'artifact' in self.image_path:
                    self.image = pygame.transform.scale(self.image, (136 // k, 136 // k))
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = artifact_cell1[0], artifact_cell1[1]
                    items_positions[self] = artifact_cell1
                    is_in_cell = True
                elif (abs(artifact_cell2[0] - self.rect.x) <= 80 and abs(artifact_cell2[1] - self.rect.y) <= 80
                        and artifact_cell2 not in items_positions.values()) and 'artifact' in self.image_path:
                    self.image = pygame.transform.scale(self.image, (136 // k, 136 // k))
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = artifact_cell2[0], artifact_cell2[1]
                    items_positions[self] = artifact_cell2
                    is_in_cell = True
                elif (abs(helmet_cell[0] - self.rect.x) <= 80 and abs(helmet_cell[1] - self.rect.y) <= 80
                        and helmet_cell not in items_positions.values()) and 'helmet' in self.image_path:
                    self.image = pygame.transform.scale(self.image, (136 // k, 136 // k))
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = helmet_cell[0], helmet_cell[1]
                    items_positions[self] = helmet_cell
                    is_in_cell = True
                elif (abs(armor_cell[0] - self.rect.x) <= 80 and abs(armor_cell[1] - self.rect.y) <= 110
                        and armor_cell not in items_positions.values()) and 'armor' in self.image_path:
                    self.image = pygame.transform.scale(self.image, (136 // k, 272 // k))
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = armor_cell[0], armor_cell[1]
                    items_positions[self] = armor_cell
                    is_in_cell = True
                elif (abs(sword_cell[0] - self.rect.x) <= 80 and abs(sword_cell[1] - self.rect.y) <= 110
                        and sword_cell not in items_positions.values()) and 'sword' in self.image_path:
                    self.image = pygame.transform.scale(self.image, (136 // k, 272 // k))
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = sword_cell[0], sword_cell[1]
                    items_positions[self] = sword_cell
                    is_in_cell = True
                elif (abs(shield_cell[0] - self.rect.x) <= 80 and abs(shield_cell[1] - self.rect.y) <= 110
                        and shield_cell not in items_positions.values()) and 'shield' in self.image_path:
                    self.image = pygame.transform.scale(self.image, (136 // k, 272 // k))
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = shield_cell[0], shield_cell[1]
                    items_positions[self] = shield_cell
                    is_in_cell = True
            if not is_in_cell:
                self.rect.x, self.rect.y = items_positions[self][0], items_positions[self][1]
            self.image.set_alpha(200)
            self.is_holding = False
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            if not self.is_holding:
                self.is_mouse_track = False
                self.image.set_alpha(255)