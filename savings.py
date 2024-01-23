import pygame
import sys
import os
import sqlite3
import subprocess

pygame.init()
with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    width = int(file.read())
    height = (width // 16) * 9
    k = 1 if width == 1920 else 1.4055636896
button_sound2 = pygame.mixer.Sound('sound_effects/button_click_4.mp3')
button_sound = pygame.mixer.Sound('sound_effects/button_click_4.mp3')
button_track_sound = pygame.mixer.Sound('sound_effects/button_tracking_04.mp3')
main_menu_music = pygame.mixer.Sound('music/main_menu_music.mp3')
screen = pygame.display.set_mode((width, height))
is_enter = False
normal_alpha = 255
hover_alpha = 215
pressed_alpha = 150
disabled_alpha = 100
font_color = (196, 183, 166)
font_color2 = (146, 107, 56)


class Save(pygame.sprite.Sprite):
    save_image = pygame.image.load('pics/save_pic.png')

    def __init__(self, y, date, width, height, *group):
        k = 1 if width == 1920 else 1.4055636896
        super().__init__(*group)
        font = pygame.font.SysFont('candara', int(30 // k), True)
        self.y = y
        self.date_text = font.render(date, True, font_color)
        self.image = pygame.transform.scale(Save.save_image, (500 // k, 50 // k))
        self.rect = self.image.get_rect()
        self.rect.x = 710 // k
        self.rect.y = y // k


class LoadButton(pygame.sprite.Sprite):
    save_image = pygame.image.load('pics/load_button.png')

    def __init__(self, y, id, width, height, *group):
        super().__init__(*group)
        k = 1 if width == 1920 else 1.4055636896
        self.y = y
        self.image = pygame.transform.scale(LoadButton.save_image, (160 // k, 39 // k))
        self.rect = self.image.get_rect()
        self.rect.x = 715 // k
        self.rect.y = (y + 5) // k
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            button_track_sound.play()
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)

