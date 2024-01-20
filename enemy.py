import pygame
import os
import random
import time


class Enemy:
    def __init__(self, x, y, width, height, max_hp, damage, speed, exp_reward):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.damage = damage
        self.speed = speed
        self.exp_reward = exp_reward
        self.direction = "down"
        self.move_frame = 0
        self.attack_frame = 0
        self.idle_frame = 0
        self.is_dead = False
        self.is_move = False
        self.is_attack = False
        self.is_damage = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.idle_frame = 0
        self.death_frame = 0
        self.death_animation_time = 0


    def load_images(self, enemy_type):
        self.move_images = {"up": [], "down": [], "left": [], "right": []}
        self.idle_images = {"up": [], "down": [], "left": [], "right": []}
        self.attack_images = {"up": [], "down": [], "left": [], "right": []}
        self.death_images = {"up": [], "down": [], "left": [], "right": []}

        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 5):
                image_path = os.path.join("data", f"{enemy_type}_move_{direction}_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.move_images[direction].append(image)
        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 5):
                image_path = os.path.join("data", f"{enemy_type}_attack_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.attack_images[direction].append(image)
                
        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 5):
                image_path = os.path.join("data", f"{enemy_type}_idle_{direction}_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.idle_images[direction].append(image)
                
        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 5):
                image_path = os.path.join("data", f"{enemy_type}_death_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.death_images[direction].append(image)
    
    def animate_idle(self):
        if not self.idle_images[self.direction]:
            return None

        self.idle_frame = (self.idle_frame + 1) % len(self.idle_images[self.direction])
        return self.idle_images[self.direction][self.idle_frame]

    
    def animate_move(self):
        self.move_frame = (self.move_frame + 1) % len(self.move_images[self.direction])
        return self.move_images[self.direction][self.move_frame]


    def animate_attack(self):
        self.attack_frame = (self.attack_frame + 1) % len(self.attack_images[self.direction])
        return self.attack_images[self.direction][self.attack_frame]


    def get_damage(self, damage_amount):
        if not self.is_dead:
            self.is_damage = True
            self.hp -= damage_amount

            self.damage_animation_time = time.time()

            if self.hp <= 0:
                self.hp = 0
                self.is_dead = True
                self.death_animation_time = time.time()


    def animate_damage(self):
        elapsed_time = time.time() - self.damage_animation_time
        if elapsed_time < 0.2:
            return (
                self.idle_images[self.direction][self.idle_frame]
                if int(elapsed_time / 0.1) % 2 == 0
                else self.get_reddish_image()
            )
        else:
            self.is_damage = False
            return (
                self.idle_images[self.direction][self.idle_frame]
                if int(elapsed_time / 0.1) % 2 == 0
                else self.get_reddish_image()
            )


    def get_reddish_image(self):
        reddish_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(reddish_image, (255, 0, 0, 128), reddish_image.get_rect())
        original_image = self.idle_images[self.direction][self.idle_frame]
        reddish_image.blit(original_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return reddish_image


    def animate_death(self):
        elapsed_time = time.time() - self.death_animation_time
        if elapsed_time < len(self.death_images[self.direction]) * 0.1:
            self.death_frame = int(elapsed_time / 0.1)
            return self.death_images[self.direction][self.death_frame]
        else:
            return -1
        

    def update_rect(self, x, y):
        self.rect.topleft = (x, y)
    

    def render_hp_bar(self, x, y, screen):
        hp_bar_width = 60
        hp_bar_height = 6
        hp_percentage = self.hp / self.max_hp - 0.01
        hp_bar_fill_width = int(hp_bar_width * hp_percentage)

        hp_bar_rect = pygame.Rect(x + self.width // 2 - hp_bar_width // 2, y - 10, hp_bar_width, hp_bar_height)
        fill_rect = pygame.Rect(x + self.width // 2 - hp_bar_width // 2, y - 10, hp_bar_fill_width, hp_bar_height)

        pygame.draw.rect(screen, (130, 87, 60), hp_bar_rect, border_radius=5, width=0) 
        pygame.draw.rect(screen, (130, 87, 60), fill_rect, border_radius=5, width=0) 

        pygame.draw.rect(screen, (92, 10, 10), hp_bar_rect.inflate(-2, -2), border_radius=3, width=0) 

        pygame.draw.rect(screen, (217, 20, 20), fill_rect.inflate(-2, -2), border_radius=3, width=0) 


class Slime(Enemy):
    def __init__(self, x, y, jump_delay=3, attack_cooldown=2):
        super().__init__(x, y, 72, 104, 60, 10, 0.1, 200)
        self.jump_delay = jump_delay
        self.attack_cooldown = attack_cooldown
        self.last_jump_time = time.time()
        self.last_attack_time = time.time()
        self.rect = pygame.Rect(self.x, self.y + 50, self.width, self.height - 50)
        self.target_x, self.target_y = self.x, self.y
        self.attack_animation_time = 0
        self.load_images("slime")


    def jump_to_random_neighbor(self):
        neighbors = [
            (self.x - 1, self.y),  # Слева
            (self.x + 1, self.y),  # Справа
            (self.x, self.y - 1),  # Вверх
            (self.x, self.y + 1)   # Вниз
        ]
        new_x, new_y = random.choice(neighbors)

        self.target_x, self.target_y = new_x, new_y
        self.last_jump_time = time.time()


    def idle(self):
        self.is_move = False
        current_time = time.time()
        if current_time - self.last_jump_time >= self.jump_delay:
            self.is_move = True
            self.jump_to_random_neighbor()


    def move(self, player_x, player_y):
        distance_to_player = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5
        if distance_to_player <= 15:
            self.speed = 0.04
            self.is_move = True
            self.target_x, self.target_y = player_x, player_y
        else:
            self.speed = 0.1
            self.idle()


    def attack(self, player):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.is_attack = True
            player.hp -= self.damage
            self.last_attack_time = current_time
            self.attack_animation_time = current_time


    def load_images(self, enemy_type):
        self.move_images = {"up": [], "down": [], "left": [], "right": []}
        self.idle_images = {"up": [], "down": [], "left": [], "right": []}
        self.attack_images = {"up": [], "down": [], "left": [], "right": []}
        self.death_images = {"up": [], "down": [], "left": [], "right": []}

        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 5):
                image_path = os.path.join("data", f"{enemy_type}_move_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.move_images[direction].append(image)

        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 5):
                image_path = os.path.join("data", f"{enemy_type}_idle_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.idle_images[direction].append(image)

        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 7):
                image_path = os.path.join("data", f"{enemy_type}_attack_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.attack_images[direction].append(image)
                
        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 5):
                image_path = os.path.join("data", f"{enemy_type}_death_{i}.png")
                image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))
                self.death_images[direction].append(image)


    def animate(self):
        lerp_speed = self.speed 
        self.x = (1 - lerp_speed) * self.x + lerp_speed * self.target_x
        self.y = (1 - lerp_speed) * self.y + lerp_speed * self.target_y

        if self.x < self.target_x:
            self.direction = "right"
        elif self.x > self.target_x:
            self.direction = "left"
        elif self.y < self.target_y:
            self.direction = "down"
        elif self.y > self.target_y:
            self.direction = "up"

        if not self.idle_images[self.direction]:
            return None
        
        if self.is_dead:
            death_animation = self.animate_death()
            print(death_animation)
            return death_animation
        if self.is_damage:
            damaged_image = self.animate_damage()
            print(damaged_image)
            return damaged_image
        if self.is_attack:
            elapsed_time = time.time() - self.attack_animation_time
            if elapsed_time < len(self.attack_images[self.direction]) * 0.1:  
                self.attack_frame = int(elapsed_time / 0.1)  
                return self.attack_images[self.direction][self.attack_frame]
            else:
                self.is_attack = False
        if self.is_move:
            self.move_frame = (self.move_frame + 1) % len(self.move_images[self.direction])
            return self.move_images[self.direction][self.move_frame]
        else:
            self.idle_frame = (self.idle_frame + 1) % len(self.idle_images[self.direction])
            return self.idle_images[self.direction][self.idle_frame]
        