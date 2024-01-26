import pygame
import sys
import os
import character_editor
import sqlite3
import start_screen
from character_editor import PlusButton
from character_editor import MinusButton
from savings import Save, LoadButton

start_screen.start_screen()


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    width = int(file.read())
    height = (width // 16) * 9
    k = 1 if width == 1920 else 1.4055636896
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 100
running = True
is_character_editor = False
is_options = False
is_music = False
is_savings = False
button_sound = pygame.mixer.Sound('sound_effects/button_click_3.mp3')
button_track_sound = pygame.mixer.Sound('sound_effects/button_tracking_04.mp3')
main_menu_music = pygame.mixer.Sound('music/main_menu_music.mp3')
normal_alpha = 255
hover_alpha = 215
pressed_alpha = 150
disabled_alpha = 100
with open('is_music.txt', mode='r', encoding='utf-8') as file:
    if file.read() == 'True':
        m_music = main_menu_music.play()
        is_music = True


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


class NewGameButton(pygame.sprite.Sprite):
    image_play_button = load_image('pics/new_game_button.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(NewGameButton.image_play_button.get_width() / (2560 / width))
        image_height = round(NewGameButton.image_play_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(NewGameButton.image_play_button,
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
            init_editor()
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class ContinueGameButton(pygame.sprite.Sprite):
    image_continue_game_button = load_image('pics/continue_game_button.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(ContinueGameButton.image_continue_game_button.get_width() / (2560 / width))
        image_height = round(ContinueGameButton.image_continue_game_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(ContinueGameButton.image_continue_game_button,
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
            init_savings()
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
        self.rect.y = height // 2.16
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
        self.rect.y = height // 1.8
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
        self.rect.x = width // 2.16949152542
        self.rect.y = height // 3.72413793103
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
        self.rect.x = width // 1.81132075472
        self.rect.y = height // 3.72413793103
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


class OnMusicButton(pygame.sprite.Sprite):
    image_on_button = load_image('pics/on_button.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(OnMusicButton.image_on_button.get_width() / (2560 / width))
        image_height = round(OnMusicButton.image_on_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(OnMusicButton.image_on_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2.16949152542
        self.rect.y = height // 2.7
        self.is_mouse_track = False

    def update(self, *args):
        global is_music, m_music
        with open('is_music.txt', mode='r', encoding='utf-8') as file:
            if file.read() == 'False':
                self.image.set_alpha(normal_alpha)
            else:
                self.image.set_alpha(disabled_alpha)
        if self.image.get_alpha() != disabled_alpha:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                self.image.set_alpha(disabled_alpha)
                button_sound.play()
                with open('is_music.txt', mode='w', encoding='utf-8') as file:
                    file.write('True')
                    if is_music:
                        m_music.set_volume(1)
                    else:
                        m_music = main_menu_music.play()
                        is_music = True
            if args and args[0].type == pygame.MOUSEMOTION and \
                    self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
                button_track_sound.play()
                self.is_mouse_track = True
            elif args and args[0].type == pygame.MOUSEMOTION and \
                    not self.rect.collidepoint(args[0].pos):
                self.is_mouse_track = False


class OffMusicButton(pygame.sprite.Sprite):
    image_off_button = load_image('pics/off_button.png')

    def __init__(self, *group):
        super().__init__(*group)
        image_width = round(OffMusicButton.image_off_button.get_width() / (2560 / width))
        image_height = round(OffMusicButton.image_off_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(OffMusicButton.image_off_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.87317073171
        self.rect.y = height // 2.7
        self.is_mouse_track = False

    def update(self, *args):
        with open('is_music.txt', mode='r', encoding='utf-8') as file:
            if file.read() == 'True':
                self.image.set_alpha(normal_alpha)
            else:
                self.image.set_alpha(disabled_alpha)
        if self.image.get_alpha() != disabled_alpha:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                self.image.set_alpha(disabled_alpha)
                button_sound.play()
                with open('is_music.txt', mode='w', encoding='utf-8') as file:
                    file.write('False')
                    m_music.set_volume(0)
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
    global background, menu_back, new_game_button, exit_button, options_button, \
        defin_button1, defin_button2, back_button, is_options, on_music_button, off_music_button, continue_game_button
    defin_button1.kill()
    defin_button2.kill()
    back_button.kill()
    on_music_button.kill()
    off_music_button.kill()
    background = Background(all_sprites)
    menu_back = Menu(all_sprites)
    new_game_button = NewGameButton(all_sprites)
    continue_game_button = ContinueGameButton(all_sprites)
    exit_button = ExitButton(all_sprites)
    options_button = OptionsButton(all_sprites)
    is_options = False


def init_options():
    global defin_button1, defin_button2, back_button, img_resolution, is_options, on_music_button, off_music_button, img_music
    new_game_button.kill()
    continue_game_button.kill()
    exit_button.kill()
    options_button.kill()
    defin_button1 = ResolutionButton1(all_sprites)
    defin_button2 = ResolutionButton2(all_sprites)
    back_button = BackButton(all_sprites)
    on_music_button = OnMusicButton(all_sprites)
    off_music_button = OffMusicButton(all_sprites)
    is_options = True
    with open('what_definition.txt', mode='r', encoding='utf-8') as file:
        if file.read() == '1920':
            k = 1
        else:
            k = 1.4055636896
        font = pygame.font.SysFont('candara', int(35 // k))
        img_resolution = font.render('Разрешение:', True, (146, 107, 56))
        img_music = font.render('Музыка:', True, (146, 107, 56))


def init_editor():
    global editor_back, is_character_editor, character_name_editor_back, enter_button, save_button
    new_game_button.kill()
    continue_game_button.kill()
    exit_button.kill()
    options_button.kill()
    menu_back.kill()
    editor_back = character_editor.EditorBack(width, height, all_sprites)
    character_name_editor_back = character_editor.CharacterNameEditorBack(width, height, all_sprites)
    enter_button = character_editor.EnterButton(width, height, all_sprites)
    save_button = character_editor.SaveButton(width, height, all_sprites)

    connect = sqlite3.connect('game.db')
    cur = connect.cursor()

    cur.execute('SELECT MAX(id) FROM characteristics')
    max_id = cur.fetchone()[0]

    if max_id is None:
        max_id = 0

    new_id = max_id + 1

    cur.close()
    connect.close()

    plus_button_1 = PlusButton(width, height, (width // 1.66956521739, height // 1.66666666667),
                               'strength', new_id, all_sprites)
    plus_button_2 = PlusButton(width, height, (width // 1.66956521739, height // 1.50627615063),
                               'endurance', new_id, all_sprites)
    plus_button_3 = PlusButton(width, height, (width // 1.66956521739, height // 1.37404580153),
                               'iq', new_id, all_sprites)
    plus_button_4 = PlusButton(width, height, (width // 1.66956521739, height // 1.26315789474),
                               'body_type', new_id, all_sprites)

    minus_button_1 = MinusButton(width, height, (width // 1.72972972973, height // 1.66666666667),
                                 'strength', new_id, all_sprites)
    minus_button_2 = MinusButton(width, height, (width // 1.72972972973, height // 1.50627615063),
                                 'endurance', new_id, all_sprites)
    minus_button_3 = MinusButton(width, height, (width // 1.72972972973, height // 1.37404580153),
                                 'iq', new_id, all_sprites)
    minus_button_4 = MinusButton(width, height, (width // 1.72972972973, height // 1.26315789474),
                                 'body_type', new_id, all_sprites)

    black_background = character_editor.BlackBackground(width, height, all_sprites)
    continue_button = character_editor.ContinueButton(width, height, all_sprites)

    is_character_editor = True

    with open('what_definition.txt', mode='r', encoding='utf-8') as file:
        if file.read() == '1920':
            k = 1
        else:
            k = 1.4055636896
        character_editor.font1 = pygame.font.SysFont('candara', int(50 // k))
        character_editor.font2 = pygame.font.SysFont('candara', int(22 // k), True)
        character_editor.img1 = character_editor.font1.render('5', True, character_editor.font_color)
        character_editor.img2 = character_editor.font1.render('5', True, character_editor.font_color)
        character_editor.img3 = character_editor.font1.render('5', True, character_editor.font_color)
        character_editor.img4 = character_editor.font1.render('5', True, character_editor.font_color)
        character_editor.line_text = character_editor.font1.render('______________',
                                                                   True, 'black')
        character_editor.name_text = character_editor.font2.render('',
                                                                   True, character_editor.font_color)

    connect = sqlite3.connect('game.db')
    cur = connect.cursor()

    cur.execute('''
        INSERT INTO characteristics (strength, endurance, iq, body_type, name)
        VALUES (?, ?, ?, ?, ?)
    ''', (5, 5, 5, 5, ''))

    connect.commit()
    cur.close()
    connect.close()


def init_savings():
    global is_savings
    menu_back.kill()
    new_game_button.kill()
    continue_game_button.kill()
    exit_button.kill()
    options_button.kill()
    connect = sqlite3.connect('game.db')
    cur = connect.cursor()
    savings = cur.execute('''
        SELECT date, id FROM savings
        ORDER BY date DESC
    ''').fetchall()
    print(savings)
    y = 20
    for i in savings:
        save = Save(y, i[0], width, height, all_sprites)
        load_button = LoadButton(y, i[1], width, height, all_sprites)
        y += 65

    is_savings = True


all_sprites = pygame.sprite.Group()
background = Background(all_sprites)
menu_back = Menu(all_sprites)
new_game_button = NewGameButton(all_sprites)
continue_game_button = ContinueGameButton(all_sprites)
exit_button = ExitButton(all_sprites)
options_button = OptionsButton(all_sprites)
all_sprites.draw(screen)

class MainMenu:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        self.running = True

    def load_image(self, name, colorkey=None):
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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                all_sprites.update(event)
                all_sprites.draw(screen)
                if is_character_editor:
                    screen.blit(character_editor.img1, (width // 2.34718826406, height // 1.67962674961))
                    screen.blit(character_editor.img2, (width // 1.96721311475, height // 1.51472650771))
                    screen.blit(character_editor.img3, (width // 2.09378407852, height // 1.37931034483))
                    screen.blit(character_editor.img4, (width // 1.9452887538, height // 1.26909518214))
                    character_editor.hint_text_blit(width, height)
                    screen.blit(character_editor.line_text, (width // 11.2280701754, height // 3.85714285714))
                    if character_editor.is_enter:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                character_editor.name = character_editor.name[:-1]
                            else:
                                character_editor.name += event.unicode if len(character_editor.name) <= 30 else 'f'
                            character_editor.name_text = character_editor.font2.render(character_editor.name,
                                                                                       True, character_editor.font_color)
                    screen.blit(character_editor.name_text, (width // 11.2280701754, height // 3.49514563107))
                if is_options:
                    with open('what_definition.txt', mode='r', encoding='utf-8') as file:
                        if file.read() == '1920':
                            k = 1
                        else:
                            k = 1.4055636896
                        font = pygame.font.SysFont('candara', int(35 // k))
                        img_resolution = font.render('Разрешение:', True, (146, 107, 56))
                        img_music = font.render('Музыка:', True, (146, 107, 56))
                    screen.blit(img_resolution, (width // 2.86995515695, height // 3.6))
                    screen.blit(img_music, (width // 2.86995515695, height // 2.66666666667))
                if is_savings:
                    with open('what_definition.txt', mode='r', encoding='utf-8') as file:
                        if file.read() == '1920':
                            k = 1
                        else:
                            k = 1.4055636896
                    for i in all_sprites:
                        if i.rect.x == 710 // k:
                            screen.blit(i.date_text, (1000 // k, (i.y + 10) // k))
                pygame.display.update()
                pygame.display.flip()
            clock.tick(fps)

        pygame.quit()