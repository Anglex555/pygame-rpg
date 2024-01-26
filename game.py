import pygame
import sys
import os
import subprocess
from hero import Hero
from item import Item
from house import House1
from house import House2
from house import House3
from house import House4
from house import House5
from house import House6
from tree import Oak
from tree import SmallOak
from tree import Spruce
from tree import Pine
from tree import SnowPine
from tree import SwampOak
from tree import DecorativeTree
from tree import DarkTree
from tree import DesertTree
from tree import MagicTree
from tree import TropicalTree
from enemy import Slime
from interface import draw_interface
from inventory import Inventory, InventoryItem, cells, items_positions, description_text_blit
from end_screen import end_screen

with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    SCREEN_WIDTH = int(file.read())
    SCREEN_HEIGHT = (SCREEN_WIDTH // 16) * 9
TILE_SIZE = 40  
ORIGINAL_TILE_SIZE = 30

DEEP_WATER_COLOR = (0, 50, 180)
SHELF_COLOR = (0, 191, 255)
SHALLOW_WATER_COLOR = (0, 255, 255)
SAND_COLOR = (245, 222, 179)
SOIL_COLOR = (144, 238, 144)
FOREST_FLOOR_COLOR = (0, 128, 0)

FPS = 50

class Game:
    def __init__(self, save):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        new_start_x = 20000
        new_start_y = 22000
        self.hero = Hero(new_start_x, new_start_y, 80, 124, 20, save)
        print(f"Name: {self.hero.name}")
        print(f"Strength: {self.hero.strength}")
        print(f"Endurance: {self.hero.endurance}")
        print(f"IQ: {self.hero.iq}")
        print(f"Body Type: {self.hero.body_type}")

        self.is_inventory = False

        sword_disc = ['Наносит урон врагам на', 'близких расстояниях']
        shield_disc = ['Защищает тело от физи-', 'ческого урона при ис-', 'пользовании']
        armor_disc = ['Защищает туловище от фи-', 'зического урона']
        jam_disc = ['Прибавляет [x] ед. здоро-', 'вья']
        helmet_disc = ['Защищает голову от фи-', 'зического урона']
        artifact1_disc = ['Прибавляет +5% к урону']
        artifact2_disc = ['Прибавляет +5% к защите']
        potion_hp_disc = ['Прибавляет 25 ед. здоровья', 'при использовании']
        potion_mana_disc = ['Прибавляет 25 ед. маны', 'при использовании']

        self.descriptions = {
            'Меч': sword_disc, 'Щит': shield_disc, 'Броня': armor_disc, 'Джем': jam_disc,
            'Шлем': helmet_disc, 'Артефакт1': artifact1_disc, 'Артефакт2': artifact2_disc,
            'Зелье_хп': potion_hp_disc, 'Зелье_мана': potion_mana_disc
        }

        pygame.init()

        img = pygame.Surface([136, 272])
        img.fill('white')
        img.set_alpha(100)

        self.blackout = (pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT]))

        with open("map.txt", "r") as file:
            map_lines = file.readlines()

        self.MAP_WIDTH = len(map_lines[0].split())
        self.MAP_HEIGHT = len(map_lines)


        self.objects = [[None for _ in range(self.MAP_WIDTH * 2)] for _ in range(self.MAP_HEIGHT * 2)]
        self.enemies = [[[] for _ in range(self.MAP_WIDTH * 2)] for _ in range(self.MAP_HEIGHT * 2)]
        self.monsters = []
        self.items = []
        self.collision_objects = []

        deep_water_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "deep_water.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        shelf_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "shelf.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        shallow_water_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "shallow_water.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        sand_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "sand.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        track_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "track.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        swamps_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "swamps.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        deep_swamps_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "deep_swamps.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        desert_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "desert.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        dune_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "dune.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        soil_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "soil.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        forest_floor_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "forest_floor.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        tropical_soil_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "tropical_soil.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        jungle_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "jungle.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        dark_earth_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "dark_earth.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        sinister_forest_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "sinister_forest.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        snowy_ground_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "snowy_ground.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        frozen_forest_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "frozen_forest.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        burning_soil_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "burning_soil.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        abyss_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "abyss.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
        road_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "road.png")), (TILE_SIZE + 20, TILE_SIZE + 20))

        with open("map.txt", "r") as file:
            self.tile_map = [list(map(int, line.strip().split())) for line in file]

        with open("objects_map.txt", "r") as file:
            self.objects_map = [list(map(int, line.strip().split())) for line in file]

        for row in range(self.MAP_HEIGHT):
            for col in range(self.MAP_WIDTH):
                object_type = self.objects_map[row][col]
                if object_type == 1:
                    self.collision_objects.append(House3(col, row))
                elif object_type == 2: 
                    self.collision_objects.append(Pine(col, row))
                elif object_type == 3: 
                    self.collision_objects.append(House5(col, row))
                elif object_type == 4: 
                    self.collision_objects.append(House3(col, row))
        for item in self.collision_objects:
            self.objects[item.x][item.y] = item

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera_window_x = 200
        self.camera_window_y = 100

        self.current_scale = 1.0
        self.min_scale = 0.5
        self.max_scale = 1.5

        self.tile_images = {
            0: {"image": deep_water_image, "depth": 0},
            1: {"image": shelf_image, "depth": 1},
            2: {"image": shallow_water_image, "depth": 2},
            3: {"image": sand_image, "depth": 3},
            4: {"image": track_image, "depth": 4},
            5: {"image": swamps_image, "depth": 5},
            6: {"image": deep_swamps_image, "depth": 6},
            7: {"image": desert_image, "depth": 7},
            8: {"image": dune_image, "depth": 8},
            9: {"image": soil_image, "depth": 9},
            10: {"image": forest_floor_image, "depth": 10},
            11: {"image": tropical_soil_image, "depth": 11},
            12: {"image": jungle_image, "depth": 12},
            13: {"image": dark_earth_image, "depth": 13},
            14: {"image": sinister_forest_image, "depth": 14},
            15: {"image": soil_image, "depth": 15},
            16: {"image": forest_floor_image, "depth": 16},
            17: {"image": burning_soil_image, "depth": 17},
            18: {"image": abyss_image, "depth": 18},
            19: {"image": road_image, "depth": 19},
        }

        object_mapping = {
            None: 0,
            Oak: 1,
            Spruce: 2,
            House1: 3,
            House2: 4
        }

        is_water = False
        self.hero.x = new_start_x
        self.hero.y = new_start_y

        self.hero.prev_x = self.hero.x
        self.hero.prev_y = self.hero.y

        self.hero.camera_x = SCREEN_WIDTH // 2 - self.hero.width // 2
        self.hero.camera_y = SCREEN_HEIGHT // 2 - self.hero.height // 2

        self.inventory_sprites = pygame.sprite.Group()
        self.inventory_back = Inventory(self.inventory_sprites)

        slime = Slime(482, 541)
        self.enemies[slime.x][slime.y].append(slime)
        self.monsters.append(self.enemies[slime.x][slime.y][-1])

        slime = Slime(486, 527)
        self.enemies[slime.x][slime.y].append(slime)
        self.monsters.append(self.enemies[slime.x][slime.y][-1])

        slime = Slime(492, 532)
        self.enemies[slime.x][slime.y].append(slime)
        self.monsters.append(self.enemies[slime.x][slime.y][-1])

        slime = Slime(472, 541)
        self.enemies[slime.x][slime.y].append(slime)
        self.monsters.append(self.enemies[slime.x][slime.y][-1])

        slime = Slime(462, 512)
        self.enemies[slime.x][slime.y].append(slime)
        self.monsters.append(self.enemies[slime.x][slime.y][-1])

        self.items.append(Item(140, 90, 60, 60, 'Джем', os.path.join("data", "jam.png")))
        self.items.append(Item(160, 100, 60, 60, 'Броня', os.path.join("pics", "armor.png")))
        self.items.append(Item(140, 100, 60, 60, 'Джем', os.path.join("data", "jam.png")))
        self.items.append(Item(160, 95, 60, 60, 'Джем', os.path.join("data", "jam.png")))
        self.items.append(Item(160, 110, 60, 60, 'Меч', os.path.join("pics", "sword.png")))
        self.items.append(Item(160, 90, 60, 60, 'Артефакт1', os.path.join("pics", "artifact_ring1.png")))
        self.items.append(Item(140, 90, 60, 60, 'Зелье_хп', os.path.join("pics", "potion_hp.png")))
        self.items.append(Item(140, 30, 60, 60, 'Шлем', os.path.join("pics", "helmet.png")))
        self.items.append(Item(140, 30, 60, 60, 'Шлем', os.path.join("pics", "helmet3.png")))
        self.items.append(Item(140, 40, 60, 60, 'Артефакт2', os.path.join("pics", "artifact_ring2.png")))
        self.items.append(Item(140, 10, 60, 60, 'Щит', os.path.join("pics", "shield.png")))
        self.items.append(Item(140, 50, 60, 60, 'Щит', os.path.join("pics", "shield2.png")))
        self.items.append(Item(140, 140, 60, 60, 'Броня', os.path.join("pics", "armor2.png")))
        self.items.append(Item(50, 110, 60, 60, 'Меч', os.path.join("pics", "sword2.png")))
        self.items.append(Item(30, 30, 60, 60, 'Шлем', os.path.join("pics", "helmet2.png")))
        self.items.append(Item(46, 35, 60, 60, 'Зелье_мана', os.path.join("pics", "potion_mana.png")))

        for item in self.items:
            self.objects[item.x][item.y] = item

        for item in self.items:
            self.hero.pick_up_item(item)
        self.clock = pygame.time.Clock()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            if self.hero.hp <= 0:
                end_screen(5 - len(self.monsters))
                self.running = False
            for event in pygame.event.get():
                if self.is_inventory:
                    self.inventory_sprites.update(event)
                    self.screen.blit(self.blackout, (0, 0))
                    self.inventory_sprites.draw(self.screen)
                    if event.type == pygame.MOUSEMOTION:
                        for i in self.hero.inventory:
                            for j in items_positions:
                                if i.unique_indx == j.unique_indx:
                                    if j.is_mouse_track and not j.is_holding:
                                        description_text_blit(event.pos[0] + 20, event.pos[1] + 20, self.descriptions[j.name], j.name)
                                        break
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    self.current_scale = min(self.current_scale + 0.1, self.max_scale)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: 
                    self.current_scale = max(self.current_scale - 0.1, self.min_scale)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        if not self.is_inventory:
                            if self.hero.inventory:
                                n = 0
                                for i in self.hero.inventory:
                                    if not i.inventory_position:
                                        inventory_item = InventoryItem(n, i.image, i.image_path, i.inventory_position,
                                                                    i.unique_indx, i.name, self.hero, self.inventory_sprites)
                                        n += 1
                                    else:
                                        inventory_item = InventoryItem(None, i.image, i.image_path, i.inventory_position,
                                                                    i.unique_indx, i.name, self.hero, self.inventory_sprites)
                        self.is_inventory = True
                    elif event.key == pygame.K_ESCAPE:
                        self.is_inventory = False
                        for i in self.inventory_sprites:
                            if i != self.inventory_back:
                                i.kill()
                        for i in items_positions.copy():
                            del items_positions[i]
                    elif event.key == pygame.K_f:
                        for item in self.items:
                            item.rect.x = item.x * TILE_SIZE + scaled_offset_x 
                            item.rect.y = item.y * TILE_SIZE + scaled_offset_y
                            if self.hero.rect.colliderect(item.rect):
                                self.hero.pick_up_item(item)
                                self.items.remove(item)
                                self.objects[item.x][item.y] = None
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    keys = pygame.key.get_pressed()

                    self.hero.attack(self.monsters, keys)

            if not self.is_inventory:
                tile_under_player = self.tile_map[(self.hero.y + self.hero.camera_y - 100) // TILE_SIZE - 10][(self.hero.x + self.hero.camera_x - 100) // TILE_SIZE - 10]
                in_water = tile_under_player in [0, 2] 

                keys = pygame.key.get_pressed()
                self.hero.move(keys, self.MAP_HEIGHT, self.MAP_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, self.camera_window_y, self.camera_window_x, self.collision_objects)

                interpolation_factor = 0.1
                self.hero_x_interp = self.hero.x + interpolation_factor * (self.hero.x - self.hero.prev_x)
                self.hero_y_interp = self.hero.y + interpolation_factor * (self.hero.y - self.hero.prev_y)

                offset_x = SCREEN_WIDTH // 2 - self.hero_x_interp - self.hero.width // 2
                offset_y = SCREEN_HEIGHT // 2 - self.hero_y_interp - self.hero.height // 2

                start_col = max(0, int(-offset_x / TILE_SIZE))
                end_col = min(self.MAP_WIDTH, int((SCREEN_WIDTH - offset_x) / TILE_SIZE) + 1)
                start_row = max(0, int(-offset_y / TILE_SIZE))
                end_row = min(self.MAP_HEIGHT, int((SCREEN_HEIGHT - offset_y) / TILE_SIZE) + 1)
                is_water = False
                
                for depth in range(20):
                    for row in range(start_row, end_row):
                        for col in range(start_col, end_col):
                            tile_type = self.tile_map[row][col]
                            tile_info = self.tile_images.get(tile_type)
                            if tile_info and tile_info["depth"] == depth:
                                scaled_tile_size = int(TILE_SIZE * self.current_scale)
                                scaled_offset_x = int(offset_x * self.current_scale)
                                scaled_offset_y = int(offset_y * self.current_scale)
                                scaled_tile_image = pygame.transform.scale(tile_info["image"], (scaled_tile_size + 8*self.current_scale, scaled_tile_size + 8*self.current_scale))
                                self.screen.blit(scaled_tile_image, (col * scaled_tile_size + scaled_offset_x, row * scaled_tile_size + scaled_offset_y))
                                
                                
                                if tile_type in [0, 1, 2]:
                                    water_rect = pygame.Rect(col * scaled_tile_size + scaled_offset_x, row * scaled_tile_size + scaled_offset_y, scaled_tile_size, scaled_tile_size)
                                    if water_rect.colliderect(self.hero.rect):
                                        neighboring_tiles = [
                                            self.tile_map[row - 1][col],  # Тайл выше
                                            self.tile_map[row + 1][col],  # Тайл ниже
                                            self.tile_map[row][col - 1],  # Тайл слева
                                            self.tile_map[row][col + 1]   # Тайл справа
                                        ]
                                        if all(neighbor_tile < 3 for neighbor_tile in neighboring_tiles):
                                            is_water = True
                
                for row in range(start_col - 15, end_col + 15):
                    for col in range(start_row - 15, end_row + 15):
                        object = self.objects[row][col]
                        if object and object.y * TILE_SIZE + scaled_offset_y < self.hero.camera_y - 200:
                            self.screen.blit(object.image, (object.x * TILE_SIZE + scaled_offset_x, object.y * TILE_SIZE + scaled_offset_y))
                        
                        for enemy in self.enemies[row][col]:
                            if enemy and enemy.y * TILE_SIZE + scaled_offset_y < self.hero.camera_y + 10:
                                enemy.update_rect(enemy.x * TILE_SIZE + scaled_offset_x , enemy.y * TILE_SIZE + scaled_offset_y + 50)
                                # pygame.draw.rect(self.screen, (125, 255, 125), enemy.rect, 2)
                                enemy.move((self.hero.x + self.hero.camera_x - 100) // TILE_SIZE - 20, (self.hero.y + self.hero.camera_y - 100) // TILE_SIZE - 8)
                                self.enemies[row][col].remove(enemy)
                                self.enemies[int(enemy.x)][int(enemy.y)].append(enemy)

                                if int(enemy.x) <= row and int(enemy.y) <= col:
                                    if self.hero.rect.colliderect(enemy.rect):
                                        enemy.attack(self.hero)
                                    enemy_image = enemy.animate()
                                    if enemy_image == -1:
                                        self.enemies[row][col].remove(enemy)
                                        self.hero.add_exp(enemy.exp_reward)
                                        self.monsters.remove(enemy)
                                    else:
                                        scaled_enemy_image = pygame.transform.scale(enemy_image, (enemy.width, enemy.height))
                                        self.screen.blit(scaled_enemy_image, (enemy.x * TILE_SIZE + scaled_offset_x, enemy.y * TILE_SIZE + scaled_offset_y))
                                        enemy.render_hp_bar(enemy.x * TILE_SIZE + scaled_offset_x , enemy.y * TILE_SIZE + scaled_offset_y + 45, self.screen)
                
                self.hero.prev_x = self.hero.x
                self.hero.prev_y = self.hero.y
                
                keys = pygame.key.get_pressed()
                hero_image = self.hero.animate(keys, is_water)
                if self.hero.is_attack:
                    self.scaled_hero_image = pygame.transform.scale(hero_image, (112, 144))
                    if self.hero.direction == "left" or self.hero.direction == "up":
                        self.screen.blit(self.scaled_hero_image, (self.hero.camera_x - 32, self.hero.camera_y))
                    else:
                        self.screen.blit(self.scaled_hero_image, (self.hero.camera_x, self.hero.camera_y))
                else:
                    self.scaled_hero_image = pygame.transform.scale(hero_image, (self.hero.width, self.hero.height))
                    self.screen.blit(self.scaled_hero_image, (self.hero.camera_x, self.hero.camera_y))

                    
                for row in range(start_col - 15, end_col + 15):
                    for col in range(start_row - 15, end_row + 15):

                        object = self.objects[row][col]

                        if object and object.y * TILE_SIZE + scaled_offset_y >= self.hero.camera_y - 200:
                            self.screen.blit(object.image, (object.x * TILE_SIZE + scaled_offset_x, object.y * TILE_SIZE + scaled_offset_y))
                        
                        for enemy in self.enemies[row][col]:
                            if enemy and enemy.y * TILE_SIZE + scaled_offset_y >= self.hero.camera_y + 10:
                                enemy.update_rect(enemy.x * TILE_SIZE + scaled_offset_x , enemy.y * TILE_SIZE + scaled_offset_y + 50)
                                # pygame.draw.rect(self.screen, (125, 255, 125), enemy.rect, 2)
                                enemy.move((self.hero.x + self.hero.camera_x - 100) // TILE_SIZE - 20, (self.hero.y + self.hero.camera_y - 100) // TILE_SIZE - 8)
                                self.enemies[row][col].remove(enemy)
                                self.enemies[int(enemy.x)][int(enemy.y)].append(enemy)

                                if int(enemy.x) <= row and int(enemy.y) <= col:
                                    if self.hero.rect.colliderect(enemy.rect):
                                        enemy.attack(self.hero)
                                    enemy_image = enemy.animate()
                                    if enemy_image == -1:
                                        self.enemies[row][col].remove(enemy)
                                        self.hero.add_exp(enemy.exp_reward)
                                        self.monsters.remove(enemy)
                                    else:
                                        scaled_enemy_image = pygame.transform.scale(enemy_image, (enemy.width, enemy.height))
                                        self.screen.blit(scaled_enemy_image, (enemy.x * TILE_SIZE + scaled_offset_x, enemy.y * TILE_SIZE + scaled_offset_y))
                                        enemy.render_hp_bar(enemy.x * TILE_SIZE + scaled_offset_x , enemy.y * TILE_SIZE + scaled_offset_y + 45, self.screen)


                self.hero.prev_x = self.hero.x
                self.hero.prev_y = self.hero.y
                
                # pygame.draw.rect(self.screen, (255, 0, 0), self.hero.rect, 2)

                # for item in self.items:
                #     pygame.draw.rect(self.screen, (125, 0, 125), item.rect, 2)
                
                for item in self.collision_objects:
                    item.update_rect(item.x * TILE_SIZE + scaled_offset_x , item.y * TILE_SIZE + scaled_offset_y)
                    # pygame.draw.rect(self.screen, (125, 0, 125), item.rect, 2)

            fps = int(self.clock.get_fps())
            font = pygame.font.Font(None, 36)
            fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
            self.screen.blit(fps_text, (1820, 10))
            
            self.hero.update_cooldown()
            draw_interface(self.screen, self.hero)

            if items_positions:
                for i in self.hero.inventory:
                    for j in items_positions:
                        if i.unique_indx == j.unique_indx and items_positions[j] not in cells:
                            i.inventory_position = items_positions[j]
                        elif i.unique_indx == j.unique_indx and items_positions[j] in cells:
                            i.inventory_position = None

            pygame.display.flip()

if __name__ == "__main__":
    game = Game(1)
    game.run()