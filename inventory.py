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
swallow_sound = pygame.mixer.Sound('sound_effects/swallow1.mp3')
clothes_on_sound = pygame.mixer.Sound('sound_effects/clothes_on2.mp3')
clothes_on_sound.set_volume(0.5)
bite_sound = pygame.mixer.Sound('sound_effects/bite1.mp3')

k = 1 if width == 1920 else 1.4055636896


def description_text_blit(x, y, text, name):
    x = x // k
    y = y // k
    black_background = pygame.Surface((200 // k, (34 + 18 * len(text)) // k))
    black_background.fill('black')
    black_background.set_alpha(200)

    font1 = pygame.font.SysFont('candara', int(16 // k), True)
    font2 = pygame.font.SysFont('candara', int(20 // k), True)
    text_coord = y + 25
    screen.blit(black_background, (x - 5, y - 5))
    name_text = font2.render(name, True, (6, 76, 249))
    screen.blit(name_text, (x, y))
    for line in text:
        string_rendered = font1.render(line, True, (146, 107, 56))
        intro_rect = string_rendered.get_rect()
        text_coord += 2
        intro_rect.top = text_coord
        intro_rect.x = x
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


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

special_cells = {
    artifact_cell1: 'artifact', artifact_cell2: 'artifact', helmet_cell: 'helmet',
    armor_cell: 'armor', sword_cell: 'sword', shield_cell: 'shield'
}

long_cells = [armor_cell, sword_cell, shield_cell]


items_positions = {}


class Inventory(pygame.sprite.Sprite):
    image_inventory = pygame.image.load('pics/whole_inventory6.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Inventory.image_inventory, (1800 // k, 597 // k))
        self.rect = self.image.get_rect()
        self.rect.x = 60 // k
        self.rect.y = 241 // k


class InventoryItem(pygame.sprite.Sprite):

    def __init__(self, indx, img, img_path, inv_pos, unique_indx, name, hero, *group):
        super().__init__(*group)
        self.hero = hero
        self.name = name
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
        self.n = 0
        self.last_mouse_pos = None

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
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 1 \
                and self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(100)
            self.is_holding = True
            self.cursor_pos[0] = args[0].pos[0] - self.rect.x
            self.cursor_pos[1] = args[0].pos[1] - self.rect.y
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 3 \
                and self.rect.collidepoint(args[0].pos) and not self.is_holding:
            is_used = False
            if self.name == 'Зелье_хп':
                self.hero.hp = self.hero.hp + 25 if self.hero.hp + 25 <= 100 else 100
                is_used = True
                swallow_sound.play()
            elif self.name == 'Зелье_мана':
                self.hero.mana = self.hero.mana + 25 if self.hero.mana + 25 <= 100 else 100
                is_used = True
                swallow_sound.play()
            elif self.name == 'Джем':
                self.hero.hp = self.hero.hp + 10 if self.hero.hp + 10 <= 100 else 100
                is_used = True
                bite_sound.play()
            if is_used:
                self.kill()
                for item in self.hero.inventory.copy():
                    if item.unique_indx == self.unique_indx:
                        self.hero.inventory.remove(item)
                        break
                self.is_mouse_track = False

        if args and args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 1 \
                and self.rect.collidepoint(args[0].pos) and self.is_holding:
            is_in_cell = False
            for i in cells:
                if abs(i[0] - self.rect.x) <= 80 and abs(i[1] - self.rect.y) <= 80:
                    if i in items_positions.values():
                        if items_positions[self] in cells:
                            for j in items_positions:
                                if items_positions[j] == i:
                                    items_positions[self], items_positions[j]\
                                        = items_positions[j], items_positions[self]
                                    self.rect.x = items_positions[self][0]
                                    self.rect.y = items_positions[self][1]
                                    j.rect.x = items_positions[j][0]
                                    j.rect.y = items_positions[j][1]
                                    is_in_cell = True
                                    self.indx = cells.index(items_positions[self])
                                    j.indx = cells.index(i)
                        else:
                            for n in special_cells:
                                if items_positions[self] == n:
                                    for j in items_positions:
                                        if items_positions[j] == i:
                                            if special_cells[n] in j.image_path:
                                                items_positions[self], items_positions[j]\
                                                    = items_positions[j], items_positions[self]
                                                if n in long_cells:
                                                    self.image = pygame.transform.scale(self.image,
                                                                                        (136 // k, 136 // k))
                                                    self.rect = self.image.get_rect()
                                                    j.image = pygame.transform.scale(j.image,
                                                                                        (136 // k, 272 // k))
                                                    j.rect = j.image.get_rect()
                                                self.rect.x = items_positions[self][0]
                                                self.rect.y = items_positions[self][1]
                                                j.rect.x = items_positions[j][0]
                                                j.rect.y = items_positions[j][1]
                                                is_in_cell = True
                                                self.indx = cells.index(items_positions[self])
                                                j.indx = cells.index(i)
                                                break
                                if is_in_cell:
                                    clothes_on_sound.play()
                                    break
                    if is_in_cell:
                        break
                    else:
                        self.image = pygame.transform.scale(self.image, (136 // k, 136 // k))
                        self.rect = self.image.get_rect()
                        self.rect.x, self.rect.y = i[0], i[1]
                        is_in_cell = True
                        self.indx = cells.index(i)
                        items_positions[self] = (i[0], i[1])
            if not is_in_cell:
                if (abs(artifact_cell1[0] - self.rect.x) <= 80 and abs(artifact_cell1[1] - self.rect.y) <= 80
                        and artifact_cell1 and 'artifact' in self.image_path):
                    if artifact_cell1 in items_positions.values():
                        if items_positions[self] in cells or items_positions[self] == artifact_cell2:
                            for j in items_positions:
                                if items_positions[j] == artifact_cell1:
                                    items_positions[self], items_positions[j] \
                                        = items_positions[j], items_positions[self]
                                    self.rect.x = items_positions[self][0]
                                    self.rect.y = items_positions[self][1]
                                    j.rect.x = items_positions[j][0]
                                    j.rect.y = items_positions[j][1]
                                    is_in_cell = True
                                    self.indx = None
                                    j.indx = cells.index(items_positions[j]) if items_positions[self] in cells else None
                                    break
                    else:
                        self.image = pygame.transform.scale(self.image, (136 // k, 136 // k))
                        self.rect = self.image.get_rect()
                        self.rect.x, self.rect.y = artifact_cell1[0], artifact_cell1[1]
                        items_positions[self] = artifact_cell1
                        is_in_cell = True
                    clothes_on_sound.play()
                elif (abs(artifact_cell2[0] - self.rect.x) <= 80 and abs(artifact_cell2[1] - self.rect.y) <= 80
                        and 'artifact' in self.image_path):
                    if artifact_cell2 in items_positions.values():
                        if items_positions[self] in cells or items_positions[self] == artifact_cell1:
                            for j in items_positions:
                                if items_positions[j] == artifact_cell2:
                                    items_positions[self], items_positions[j] \
                                        = items_positions[j], items_positions[self]
                                    self.rect.x = items_positions[self][0]
                                    self.rect.y = items_positions[self][1]
                                    j.rect.x = items_positions[j][0]
                                    j.rect.y = items_positions[j][1]
                                    is_in_cell = True
                                    self.indx = None
                                    j.indx = cells.index(items_positions[j]) if items_positions[self] in cells else None
                                    break
                    else:
                        self.image = pygame.transform.scale(self.image, (136 // k, 136 // k))
                        self.rect = self.image.get_rect()
                        self.rect.x, self.rect.y = artifact_cell2[0], artifact_cell2[1]
                        items_positions[self] = artifact_cell2
                        is_in_cell = True
                    clothes_on_sound.play()
                elif (abs(helmet_cell[0] - self.rect.x) <= 80 and abs(helmet_cell[1] - self.rect.y) <= 80
                        and 'helmet' in self.image_path):
                    if helmet_cell in items_positions.values():
                        if items_positions[self] in cells:
                            for j in items_positions:
                                if items_positions[j] == helmet_cell:
                                    items_positions[self], items_positions[j] \
                                        = items_positions[j], items_positions[self]
                                    self.rect.x = items_positions[self][0]
                                    self.rect.y = items_positions[self][1]
                                    j.rect.x = items_positions[j][0]
                                    j.rect.y = items_positions[j][1]
                                    is_in_cell = True
                                    self.indx = None
                                    j.indx = cells.index(items_positions[j])
                                    break
                    else:
                        self.image = pygame.transform.scale(self.image, (136 // k, 136 // k))
                        self.rect = self.image.get_rect()
                        self.rect.x, self.rect.y = helmet_cell[0], helmet_cell[1]
                        items_positions[self] = helmet_cell
                        is_in_cell = True
                    clothes_on_sound.play()
                elif (abs(armor_cell[0] - self.rect.x) <= 80 and abs(armor_cell[1] - self.rect.y) <= 110
                        and 'armor' in self.image_path):
                    if armor_cell in items_positions.values():
                        if items_positions[self] in cells:
                            for j in items_positions:
                                if items_positions[j] == armor_cell:
                                    items_positions[self], items_positions[j] \
                                        = items_positions[j], items_positions[self]
                                    self.image = pygame.transform.scale(self.image,
                                                                        (136 // k, 272 // k))
                                    self.rect = self.image.get_rect()
                                    j.image = pygame.transform.scale(j.image,
                                                                     (136 // k, 136 // k))
                                    j.rect = j.image.get_rect()
                                    self.rect.x = items_positions[self][0]
                                    self.rect.y = items_positions[self][1]
                                    j.rect.x = items_positions[j][0]
                                    j.rect.y = items_positions[j][1]
                                    is_in_cell = True
                                    self.indx = None
                                    j.indx = cells.index(items_positions[j])
                                    break
                    else:
                        self.image = pygame.transform.scale(self.image, (136 // k, 272 // k))
                        self.rect = self.image.get_rect()
                        self.rect.x, self.rect.y = armor_cell[0], armor_cell[1]
                        items_positions[self] = armor_cell
                        is_in_cell = True
                    clothes_on_sound.play()
                elif (abs(sword_cell[0] - self.rect.x) <= 80 and abs(sword_cell[1] - self.rect.y) <= 110
                        and 'sword' in self.image_path):
                    if sword_cell in items_positions.values():
                        if items_positions[self] in cells:
                            for j in items_positions:
                                if items_positions[j] == sword_cell:
                                    items_positions[self], items_positions[j] \
                                        = items_positions[j], items_positions[self]
                                    self.image = pygame.transform.scale(self.image,
                                                                        (136 // k, 272 // k))
                                    self.rect = self.image.get_rect()
                                    j.image = pygame.transform.scale(j.image,
                                                                     (136 // k, 136 // k))
                                    j.rect = j.image.get_rect()
                                    self.rect.x = items_positions[self][0]
                                    self.rect.y = items_positions[self][1]
                                    j.rect.x = items_positions[j][0]
                                    j.rect.y = items_positions[j][1]
                                    is_in_cell = True
                                    self.indx = None
                                    j.indx = cells.index(items_positions[j])
                                    break
                    else:
                        self.image = pygame.transform.scale(self.image, (136 // k, 272 // k))
                        self.rect = self.image.get_rect()
                        self.rect.x, self.rect.y = sword_cell[0], sword_cell[1]
                        items_positions[self] = sword_cell
                        is_in_cell = True
                    clothes_on_sound.play()
                elif (abs(shield_cell[0] - self.rect.x) <= 80 and abs(shield_cell[1] - self.rect.y) <= 110
                        and 'shield' in self.image_path):
                    if shield_cell in items_positions.values():
                        if items_positions[self] in cells:
                            for j in items_positions:
                                if items_positions[j] == shield_cell:
                                    items_positions[self], items_positions[j] \
                                        = items_positions[j], items_positions[self]
                                    self.image = pygame.transform.scale(self.image,
                                                                        (136 // k, 272 // k))
                                    self.rect = self.image.get_rect()
                                    j.image = pygame.transform.scale(j.image,
                                                                     (136 // k, 136 // k))
                                    j.rect = j.image.get_rect()
                                    self.rect.x = items_positions[self][0]
                                    self.rect.y = items_positions[self][1]
                                    j.rect.x = items_positions[j][0]
                                    j.rect.y = items_positions[j][1]
                                    is_in_cell = True
                                    self.indx = None
                                    j.indx = cells.index(items_positions[j])
                                    break
                    else:
                        self.image = pygame.transform.scale(self.image, (136 // k, 272 // k))
                        self.rect = self.image.get_rect()
                        self.rect.x, self.rect.y = shield_cell[0], shield_cell[1]
                        items_positions[self] = shield_cell
                        is_in_cell = True
                    clothes_on_sound.play()
            if not is_in_cell:
                self.rect.x, self.rect.y = items_positions[self][0], items_positions[self][1]
            self.image.set_alpha(200)
            self.is_holding = False
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            if not self.is_holding:
                self.is_mouse_track = False
                self.image.set_alpha(255)