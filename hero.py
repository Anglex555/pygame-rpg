import pygame
import sys
import os

class Hero:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = "down"
        self.run_frame = 0
        self.prev_x = x 
        self.prev_y = y 
        self.camera_x = x 
        self.camera_y = y 
        self.inventory = []
        self.idle_frame = 0
        self.idle_images = {"up": [], "down": [], "left": [], "right": []}
        self.swim_images = {"up": [], "down": [], "left": [], "right": []}
        self.idle_swim_images = {"up": [], "down": [], "left": [], "right": []}
        self.swim_frame = 0
        self.load_images()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys, MAP_HEIGHT, MAP_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, camera_window_y, camera_window_x, collision_objects):
        new_x = self.x
        new_y = self.y

        new_camera_x = self.camera_x
        new_camera_y = self.camera_y

        if keys[pygame.K_w] and new_y - 1 >= 100 and self.camera_y <= (SCREEN_HEIGHT // 2) - camera_window_y - self.height:
            new_y -= self.speed
            self.direction = "up"
        if keys[pygame.K_s] and new_y + self.height + 1 <= MAP_HEIGHT * TILE_SIZE and self.camera_y >= (SCREEN_HEIGHT // 2) + camera_window_y:
            new_y += self.speed
            self.direction = "down"
        if keys[pygame.K_a] and new_x - 1 >= 200 and self.camera_x <= (SCREEN_WIDTH // 2) - camera_window_x - self.width:
            new_x -= self.speed
            self.direction = "left"
        if keys[pygame.K_d] and new_x + self.width + 1 <= MAP_WIDTH * TILE_SIZE and self.camera_x >= (SCREEN_WIDTH // 2) + camera_window_x:
            new_x += self.speed
            self.direction = "right"
        
        if keys[pygame.K_w] and new_y - 1 >= 0 and self.camera_y > (SCREEN_HEIGHT // 2) - camera_window_y - self.height:
            new_camera_y -= self.speed
            self.direction = "up"
        if keys[pygame.K_s] and new_y + self.height + 1 <= MAP_HEIGHT * TILE_SIZE and self.camera_y < (SCREEN_HEIGHT // 2) + camera_window_y:
            new_camera_y += self.speed
            self.direction = "down"
        if keys[pygame.K_a] and new_x - 1 >= 0 and self.camera_x > (SCREEN_WIDTH // 2) - camera_window_x - self.width:
            new_camera_x -= self.speed
            self.direction = "left"
        if keys[pygame.K_d] and new_x + self.width + 1 <= MAP_WIDTH * TILE_SIZE and self.camera_x < (SCREEN_WIDTH // 2) + camera_window_x:
            new_camera_x += self.speed
            self.direction = "right"
        
        temp_rect = pygame.Rect(new_camera_x, new_camera_y, self.width, self.height)
    
        if not self.check_collision(collision_objects, temp_rect):
            self.x = new_x
            self.y = new_y
            self.camera_x = new_camera_x
            self.camera_y = new_camera_y

        self.rect.x = self.camera_x
        self.rect.y = self.camera_y
            
    def check_collision(self, objects, temp_rect):
        for object in objects:
            if object and temp_rect.colliderect(object.rect):
                return True  # Коллизия обнаружена
        return False  # Нет коллизии

    def load_images(self):
        self.run_images = {"up": [], "down": [], "left": [], "right": []}
        self.idle_images = {"up": [], "down": [], "left": [], "right": []}
        self.swim_images = {"up": [], "down": [], "left": [], "right": []}
        self.idle_swim_images = {"up": [], "down": [], "left": [], "right": []}

        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 7):
                image_path = os.path.join("data", f"player_run_{direction}_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.run_images[direction].append(image)

        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 7):
                image_path = os.path.join("data", f"player_idle_{direction}_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.idle_images[direction].append(image)

        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 7): 
                image_path = os.path.join("data", f"player_swim_{direction}_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.swim_images[direction].append(image)

        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 7): 
                image_path = os.path.join("data", f"player_idle_swim_{direction}_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.idle_swim_images[direction].append(image)

    def animate(self, keys, in_water):
        if not any((keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d])):
            if in_water:
                # Анимация спокойствия в воде
                self.idle_frame = (self.idle_frame + 1) % len(self.idle_swim_images[self.direction])
                return self.idle_swim_images[self.direction][self.idle_frame]
            else:
                # Анимация спокойствия
                self.idle_frame = (self.idle_frame + 1) % len(self.idle_images[self.direction])
                return self.idle_images[self.direction][self.idle_frame]
        else:
            if in_water:
                # Анимация плавания
                self.swim_frame = (self.swim_frame + 1) % len(self.swim_images[self.direction])
                return self.swim_images[self.direction][self.swim_frame]
            else:
                # Анимация бега
                self.run_frame = (self.run_frame + 1) % len(self.run_images[self.direction])
                return self.run_images[self.direction][self.run_frame]

    def pick_up_item(self, item):
        self.inventory.append(item)
        print(self.inventory)

    def drop_item(self):
        # Пример: выбрасываем последний предмет из инвентаря
        if self.inventory:
            item_to_drop = self.inventory.pop()
            print(f"Dropped item at ({item_to_drop.x}, {item_to_drop.y})")