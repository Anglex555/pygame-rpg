import pygame
import sys
import os
from hero import Hero
from item import Item
from house import House
from tree import Oak
from tree import Spruce

pygame.init()

# Определение размеров окна и экрана
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
TILE_SIZE = 40
# Оригинальные размеры тайлов
ORIGINAL_TILE_SIZE = 30

MAP_WIDTH = 350
MAP_HEIGHT = 200

# Цвета для тайлов
DEEP_WATER_COLOR = (0, 50, 180)
SHELF_COLOR = (0, 191, 255)
SHALLOW_WATER_COLOR = (0, 255, 255)
SAND_COLOR = (245, 222, 179)
SOIL_COLOR = (144, 238, 144)
FOREST_FLOOR_COLOR = (0, 128, 0)

objects = [[None for _ in range(MAP_WIDTH * 2)] for _ in range(MAP_HEIGHT * 2)]
items = []
collision_objects = []

# Загрузка изображений тайлов
deep_water_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "deep_water.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
shelf_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "shelf.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
shallow_water_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "shallow_water.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
sand_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "sand.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
track_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "track.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
soil_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "soil.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
forest_floor_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "forest_floor.png")), (TILE_SIZE + 20, TILE_SIZE + 20))
road_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "road.png")), (TILE_SIZE + 20, TILE_SIZE + 20))


# Тайлы карты
with open("map.txt", "r") as file:
    tile_map = [list(map(int, line.strip().split())) for line in file]

with open("objects_map.txt", "r") as file:
    objects_map = [list(map(int, line.strip().split())) for line in file]

# Создание объектов в соответствии с картой объектов
for row in range(40):
    for col in range(40):
        object_type = objects_map[row][col]
        if object_type == 1:
            objects[row][col] = Oak(col, row)
        elif object_type == 2:
            objects[row][col] = Spruce(col, row)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile-based Pygame Map")
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
    5: {"image": soil_image, "depth": 5},
    6: {"image": forest_floor_image, "depth": 6},
    7: {"image": road_image, "depth": 7},
}

hero = Hero(MAP_WIDTH * TILE_SIZE // 2 - 80 // 2, MAP_HEIGHT * TILE_SIZE // 2 - 124 // 2, 80, 124, 20)

hero.x = 6665
hero.y = 4360

hero.prev_x = hero.x
hero.prev_y = hero.y

hero.camera_x = SCREEN_WIDTH // 2 - hero.width // 2
hero.camera_y = SCREEN_HEIGHT // 2 - hero.height // 2

items.append(Item(140, 90, 60, 60, 'джем', os.path.join("data", "jam.png")))
items.append(Item(140, 100, 60, 60, 'джем', os.path.join("data", "jam.png")))
items.append(Item(160, 95, 60, 60, 'джем', os.path.join("data", "jam.png")))

for item in items:
    objects[item.x][item.y] = item

collision_objects.append(Spruce(170, 100))
collision_objects.append(Spruce(175, 102))
collision_objects.append(Oak(150, 100))
collision_objects.append(House(180, 85, 600, 600))
collision_objects.append(House(174, 65, 600, 600))
collision_objects.append(House(204, 28, 600, 600))
    
for item in collision_objects:
    objects[item.x][item.y] = item

FPS = 13

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

    # Обработка управления кубиком

    keys = pygame.key.get_pressed()
    hero.move(keys, MAP_HEIGHT, MAP_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, camera_window_y, camera_window_x, objects)

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

    # Отображение тайлов на экране с учетом смещения и области видимости
    for depth in range(8):
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

    for depth in range(8):
        for row in range(start_col - 15, end_col + 15):
            for col in range(start_row - 15, end_row + 15):
                object = objects[row][col]
                if object and object.y < (hero.y + hero.camera_y - 100) // TILE_SIZE - 10:
                    screen.blit(object.image, (object.x * TILE_SIZE + scaled_offset_x, object.y * TILE_SIZE + scaled_offset_y))
    
    hero.prev_x = hero.x
    hero.prev_y = hero.y
    
    keys = pygame.key.get_pressed()
    hero_image = hero.animate(keys)
    scaled_hero_image = pygame.transform.scale(hero_image, (hero.width, hero.height))
    screen.blit(scaled_hero_image, (hero.camera_x, hero.camera_y))
    # print((hero.y + hero.camera_y - 100) // TILE_SIZE - 10,(hero.x + hero.camera_x - 100) // TILE_SIZE - 10)
    for depth in range(8):
        for row in range(start_col - 15, end_col + 15):
            for col in range(start_row - 15, end_row + 15):
                object = objects[row][col]
                if object and object.y >= (hero.y + hero.camera_y - 100) // TILE_SIZE - 10:
                    screen.blit(object.image, (object.x * TILE_SIZE + scaled_offset_x, object.y * TILE_SIZE + scaled_offset_y))

    # Обновление предыдущих координат игрока
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
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
