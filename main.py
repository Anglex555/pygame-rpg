import pygame
import sys
import os
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

pygame.init()

# Определение размеров окна и экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TILE_SIZE = 40
# Оригинальные размеры тайлов
ORIGINAL_TILE_SIZE = 30

with open("map.txt", "r") as file:
    map_lines = file.readlines()

MAP_WIDTH = len(map_lines[0].split())
MAP_HEIGHT = len(map_lines)

# Цвета для тайлов
DEEP_WATER_COLOR = (0, 50, 180)
SHELF_COLOR = (0, 191, 255)
SHALLOW_WATER_COLOR = (0, 255, 255)
SAND_COLOR = (245, 222, 179)
SOIL_COLOR = (144, 238, 144)
FOREST_FLOOR_COLOR = (0, 128, 0)

objects = [[None for _ in range(MAP_WIDTH * 2)] for _ in range(MAP_HEIGHT * 2)]
enemies = [[None for _ in range(MAP_WIDTH * 2)] for _ in range(MAP_HEIGHT * 2)]
monsters = []
items = []
collision_objects = []

# Загрузка изображений тайлов
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

# Тайлы карты
with open("map.txt", "r") as file:
    tile_map = [list(map(int, line.strip().split())) for line in file]

with open("objects_map.txt", "r") as file:
    objects_map = [list(map(int, line.strip().split())) for line in file]

# Создание объектов в соответствии с картой объектов
for row in range(MAP_HEIGHT):
    for col in range(MAP_WIDTH):
        object_type = objects_map[row][col]
        if object_type == 1:
            collision_objects.append(Oak(col, row))
        elif object_type == 2: 
            collision_objects.append(SnowPine(col, row))
        elif object_type == 3: 
            collision_objects.append(House5(col, row))
        elif object_type == 4: 
            collision_objects.append(House3(col, row))
for item in collision_objects:
    objects[item.x][item.y] = item

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Tile-based Pygame Map")
camera_window_x = 200
camera_window_y = 100

# Масштабирование карты
current_scale = 1.0
min_scale = 0.5
max_scale = 1.5

# Словарь для соответствия типа тайла изображению и их глубины
tile_images = {
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
    15: {"image": snowy_ground_image, "depth": 15},
    16: {"image": frozen_forest_image, "depth": 16},
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

new_start_x = 20000
new_start_y = 22000
hero = Hero(new_start_x, new_start_y, 80, 124, 20)

is_water = False
hero.x = new_start_x
hero.y = new_start_y

hero.prev_x = hero.x
hero.prev_y = hero.y

hero.camera_x = SCREEN_WIDTH // 2 - hero.width // 2
hero.camera_y = SCREEN_HEIGHT // 2 - hero.height // 2
FPS = 13
slime = Slime(482, 541)
enemies[slime.x][slime.y] = slime
monsters.append(enemies[slime.x][slime.y])
clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    # pygame.display.set_caption("FPS = " + str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Колесо вверх
            current_scale = min(current_scale + 0.1, max_scale)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Колесо вниз
            current_scale = max(current_scale - 0.1, min_scale)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                for item in items:
                    item.rect.x = item.x * TILE_SIZE + scaled_offset_x 
                    item.rect.y = item.y * TILE_SIZE + scaled_offset_y
                    if hero.rect.colliderect(item.rect):
                        hero.pick_up_item(item)
                        items.remove(item)
                        objects[item.x][item.y] = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            keys = pygame.key.get_pressed()
            hero.attack(monsters, keys)

    # Обработка управления кубиком

    tile_under_player = tile_map[(hero.y + hero.camera_y - 100) // TILE_SIZE - 10][(hero.x + hero.camera_x - 100) // TILE_SIZE - 10]
    in_water = tile_under_player in [0, 2]  # Глубокая или мелкая вода

    # Обработка управления кубиком
    keys = pygame.key.get_pressed()
    hero.move(keys, MAP_HEIGHT, MAP_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, camera_window_y, camera_window_x, collision_objects)

    # Линейная интерполяция для сглаживания движения карты
    interpolation_factor = 0.1
    hero_x_interp = hero.x + interpolation_factor * (hero.x - hero.prev_x)
    hero_y_interp = hero.y + interpolation_factor * (hero.y - hero.prev_y)

    # Пересчет смещения для отрисовки тайлов
    offset_x = SCREEN_WIDTH // 2 - hero_x_interp - hero.width // 2
    offset_y = SCREEN_HEIGHT // 2 - hero_y_interp - hero.height // 2
    # print(hero_x_interp, hero_y_interp)
    # Отображение тайлов на экране с учетом смещения
    
    start_col = max(0, int(-offset_x / TILE_SIZE))
    end_col = min(MAP_WIDTH, int((SCREEN_WIDTH - offset_x) / TILE_SIZE) + 1)
    start_row = max(0, int(-offset_y / TILE_SIZE))
    end_row = min(MAP_HEIGHT, int((SCREEN_HEIGHT - offset_y) / TILE_SIZE) + 1)
    is_water = False
    # Отображение тайлов на экране с учетом смещения и области видимости
    for depth in range(20):
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                tile_type = tile_map[row][col]
                tile_info = tile_images.get(tile_type)
                if tile_info and tile_info["depth"] == depth:
                    # Учтем масштабирование
                    scaled_tile_size = int(TILE_SIZE * current_scale)
                    scaled_offset_x = int(offset_x * current_scale)
                    scaled_offset_y = int(offset_y * current_scale)
                    scaled_tile_image = pygame.transform.scale(tile_info["image"], (scaled_tile_size + 8*current_scale, scaled_tile_size + 8*current_scale))
                    screen.blit(scaled_tile_image, (col * scaled_tile_size + scaled_offset_x, row * scaled_tile_size + scaled_offset_y))
                    
                    
                    if tile_type in [0, 1, 2]:
                        water_rect = pygame.Rect(col * scaled_tile_size + scaled_offset_x, row * scaled_tile_size + scaled_offset_y, scaled_tile_size, scaled_tile_size)
                        if water_rect.colliderect(hero.rect):
                            # Добавляем проверку, чтобы убедиться, что тайл воды не граничит с песком
                            neighboring_tiles = [
                                tile_map[row - 1][col],  # Тайл выше
                                tile_map[row + 1][col],  # Тайл ниже
                                tile_map[row][col - 1],  # Тайл слева
                                tile_map[row][col + 1]   # Тайл справа
                            ]
                            if all(neighbor_tile != 3 for neighbor_tile in neighboring_tiles):
                                is_water = True
    
    for row in range(start_col - 15, end_col + 15):
        for col in range(start_row - 15, end_row + 15):
            object = objects[row][col]
            if object and object.y < (hero.y + hero.camera_y - 100) // TILE_SIZE - 10:
                screen.blit(object.image, (object.x * TILE_SIZE + scaled_offset_x, object.y * TILE_SIZE + scaled_offset_y))
    
    hero.prev_x = hero.x
    hero.prev_y = hero.y
    
    keys = pygame.key.get_pressed()
    hero_image = hero.animate(keys, is_water)
    if hero.is_attack:
        scaled_hero_image = pygame.transform.scale(hero_image, (112, 144))
        if hero.direction == "left" or hero.direction == "up":
            screen.blit(scaled_hero_image, (hero.camera_x - 32, hero.camera_y))
        else:
            screen.blit(scaled_hero_image, (hero.camera_x, hero.camera_y))
    else:
        scaled_hero_image = pygame.transform.scale(hero_image, (hero.width, hero.height))
        screen.blit(scaled_hero_image, (hero.camera_x, hero.camera_y))
    # print((hero.y + hero.camera_y - 100) // TILE_SIZE - 10,(hero.x + hero.camera_x - 100) // TILE_SIZE - 10)
    for row in range(start_col - 15, end_col + 15):
        for col in range(start_row - 15, end_row + 15):
            object = objects[row][col]
            if object and object.y >= (hero.y + hero.camera_y - 100) // TILE_SIZE - 10:
                screen.blit(object.image, (object.x * TILE_SIZE + scaled_offset_x, object.y * TILE_SIZE + scaled_offset_y))
            enemy = enemies[row][col]
            if enemy:
                enemy.update_rect(enemy.x * TILE_SIZE + scaled_offset_x , enemy.y * TILE_SIZE + scaled_offset_y + 50)
                pygame.draw.rect(screen, (125, 255, 125), enemy.rect, 2)
                enemy.move((hero.x + hero.camera_x - 100) // TILE_SIZE - 16, (hero.y + hero.camera_y - 100) // TILE_SIZE - 6)
                enemies[row][col] = None
                enemies[int(enemy.x)][int(enemy.y)] = enemy
                if int(enemy.x) <= row and int(enemy.y) <= col:
                    if hero.rect.colliderect(enemy.rect):
                        enemy.attack(hero)
                    enemy_image = enemy.animate()
                    if enemy_image == -1:
                        enemies[row][col] = None
                        hero.add_exp(enemy.exp_reward)
                        monsters.remove(enemy)
                    else:
                        scaled_enemy_image = pygame.transform.scale(enemy_image, (enemy.width, enemy.height))
                        screen.blit(scaled_enemy_image, (enemy.x * TILE_SIZE + scaled_offset_x, enemy.y * TILE_SIZE + scaled_offset_y))
                        enemy.render_hp_bar(enemy.x * TILE_SIZE + scaled_offset_x , enemy.y * TILE_SIZE + scaled_offset_y + 45, screen)
     # Обновление состояния слизня
    hero.prev_x = hero.x
    hero.prev_y = hero.y
    
    pygame.draw.rect(screen, (255, 0, 0), hero.rect, 2)

    for item in items:
        pygame.draw.rect(screen, (125, 0, 125), item.rect, 2)
    
    for item in collision_objects:
        item.update_rect(item.x * TILE_SIZE + scaled_offset_x , item.y * TILE_SIZE + scaled_offset_y)
        pygame.draw.rect(screen, (125, 0, 125), item.rect, 2)

    # Отображение FPS
    fps = int(clock.get_fps())
    font = pygame.font.Font(None, 36)
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (1820, 10))
    
    hero.update_cooldown()
    draw_interface(screen, hero)

    pygame.display.flip()
