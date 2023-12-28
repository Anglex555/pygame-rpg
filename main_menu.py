import pygame
import sys
import os


pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 100
running = True
button_sound = pygame.mixer.Sound('sound_effects/button_click_3.mp3')
button_track_sound = pygame.mixer.Sound('sound_effects/button_tracking_04.mp3')
main_menu_music = pygame.mixer.Sound('music/main_menu_music.mp3')
normal_alpha = 255
hover_alpha = 215
pressed_alpha = 150
disabled_alpha = 100
main_menu_music.play()


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Menu(pygame.sprite.Sprite):
    image_menu_back = load_image('pics/rpg_menu_back.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Menu.image_menu_back, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Background(pygame.sprite.Sprite):
    image_background = load_image('pics/rpg_background_pixel_color_fixed.jpg')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Background.image_background, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class StartButton(pygame.sprite.Sprite):
    image_play_button = load_image('pics/play_button.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(StartButton.image_play_button.get_width() / (2560 / width))
        image_height = round(StartButton.image_play_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(StartButton.image_play_button,
                                                               (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2.72
        self.rect.y = height // 3.6
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


class OptionsButton(pygame.sprite.Sprite):
    image_options_button = load_image('pics/options_button.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(OptionsButton.image_options_button.get_width() / (2560 / width))
        image_height = round(OptionsButton.image_options_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(OptionsButton.image_options_button,
                                                               (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2.72
        self.rect.y = height // 2.7
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
            init_options()
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class ExitButton(pygame.sprite.Sprite):
    image_exit_button = load_image('pics/exit_button.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(ExitButton.image_exit_button.get_width() / (2560 / width))
        image_height = round(ExitButton.image_exit_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(ExitButton.image_exit_button,
                                                              (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2.72
        self.rect.y = height // 2.16
        self.is_mouse_track = False

    def update(self, *args):
        global running
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            button_track_sound.play()
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            running = False
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class ResolutionButton1(pygame.sprite.Sprite):
    image_definition_button = load_image('pics/small_button_1920.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(ResolutionButton1.image_definition_button.get_width() / (2560 / width))
        image_height = round(ResolutionButton1.image_definition_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(ResolutionButton1.image_definition_button,
                                                              (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.92
        self.rect.y = height // 3.9272727273
        self.is_mouse_track = False

    def update(self, *args):
        with open('what_definition.txt', mode='r', encoding='utf-8') as file:
            if file.read() == '1366':
                self.image.set_alpha(normal_alpha)
            else:
                self.image.set_alpha(disabled_alpha)
        if self.image.get_alpha() != disabled_alpha:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                self.image.set_alpha(disabled_alpha)
                button_sound.play()
                with open('what_definition.txt', mode='w', encoding='utf-8') as file:
                    file.write('1920')
                    change_resolution(1920, 1080)
            if args and args[0].type == pygame.MOUSEMOTION and \
                    self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
                button_track_sound.play()
                self.is_mouse_track = True
            elif args and args[0].type == pygame.MOUSEMOTION and \
                    not self.rect.collidepoint(args[0].pos):
                self.is_mouse_track = False


class ResolutionButton2(pygame.sprite.Sprite):
    image_definition_button = load_image('pics/small_button_1366.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(ResolutionButton2.image_definition_button.get_width() / (2560 / width))
        image_height = round(ResolutionButton2.image_definition_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(ResolutionButton2.image_definition_button,
                                                              (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.92
        self.rect.y = height // 2.88
        self.is_mouse_track = False

    def update(self, *args):
        with open('what_definition.txt', mode='r', encoding='utf-8') as file:
            if file.read() == '1920':
                self.image.set_alpha(normal_alpha)
            else:
                self.image.set_alpha(disabled_alpha)
        if self.image.get_alpha() != disabled_alpha:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                self.image.set_alpha(disabled_alpha)
                button_sound.play()
                with open('what_definition.txt', mode='w', encoding='utf-8') as file:
                    file.write('1366')
                change_resolution(1366, 768)
            if args and args[0].type == pygame.MOUSEMOTION and \
                    self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
                button_track_sound.play()
                self.is_mouse_track = True
            elif args and args[0].type == pygame.MOUSEMOTION and \
                    not self.rect.collidepoint(args[0].pos):
                self.is_mouse_track = False


class BackButton(pygame.sprite.Sprite):
    image_back_button = load_image('pics/back_button.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(BackButton.image_back_button.get_width() / (2560 / width))
        image_height = round(BackButton.image_back_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(BackButton.image_back_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2.86567164179
        self.rect.y = height // 4.8
        self.is_mouse_track = False

    def update(self, *args):
        global running
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            button_track_sound.play()
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            init_main_menu()
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


def change_resolution(w, h):
    global width, height, screen
    width, height = w, h
    screen = pygame.display.set_mode((width, height))
    init_main_menu()
    init_options()


def init_main_menu():
    global background, menu_back, start_button, exit_button, options_button, \
        defin_button1, defin_button2, back_button
    defin_button1.kill()
    defin_button2.kill()
    back_button.kill()
    background = Background(all_sprites)
    menu_back = Menu(all_sprites)
    start_button = StartButton(all_sprites)
    exit_button = ExitButton(all_sprites)
    options_button = OptionsButton(all_sprites)


def init_options():
    global defin_button1, defin_button2, back_button
    start_button.kill()
    exit_button.kill()
    options_button.kill()
    defin_button1 = ResolutionButton1(all_sprites)
    defin_button2 = ResolutionButton2(all_sprites)
    back_button = BackButton(all_sprites)


defin_button1, defin_button2, back_button = None, None, None

all_sprites = pygame.sprite.Group()
background = Background(all_sprites)
menu_back = Menu(all_sprites)
start_button = StartButton(all_sprites)
exit_button = ExitButton(all_sprites)
options_button = OptionsButton(all_sprites)
all_sprites.draw(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_sprites.update(event)
        all_sprites.draw(screen)
        pygame.display.flip()
    clock.tick(fps)