import pygame
import sys
import os
import sqlite3


pygame.init()
with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    width = int(file.read())
    height = (width // 16) * 9
button_sound2 = pygame.mixer.Sound('sound_effects/button_click_4.mp3')
button_sound = pygame.mixer.Sound('sound_effects/button_click_3.mp3')
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
tokens = 20
token = 5
font1 = pygame.font.SysFont('candara', 50)
font2 = pygame.font.SysFont('candara', 30, True)
img1 = font1.render('5', True, font_color)
img2 = font1.render('5', True, font_color)
img3 = font1.render('5', True, font_color)
img4 = font1.render('5', True, font_color)

line_text = font1.render('________________________', True, 'black')
name = ''
name_text = font1.render('', True, font_color)

characteristics = {'strength': img1, 'endurance': img2, 'iq': img3, 'body_type': img4}

lower_letters_event = {
    pygame.K_a: 'a', pygame.K_b: 'b', pygame.K_c: 'c', pygame.K_d: 'd', pygame.K_e: 'e',
    pygame.K_f: 'f', pygame.K_g: 'g', pygame.K_h: 'h', pygame.K_i: 'i', pygame.K_j: 'j',
    pygame.K_k: 'k', pygame.K_l: 'l', pygame.K_m: 'm', pygame.K_n: 'n', pygame.K_o: 'o',
    pygame.K_p: 'p', pygame.K_q: 'q', pygame.K_r: 'r', pygame.K_s: 's', pygame.K_t: 't',
    pygame.K_u: 'u', pygame.K_v: 'v', pygame.K_w: 'w', pygame.K_x: 'x', pygame.K_y: 'y',
    pygame.K_z: 'z',
}

upper_letters_event = {
    pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D', pygame.K_e: 'E',
    pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H', pygame.K_i: 'I', pygame.K_j: 'J',
    pygame.K_k: 'K', pygame.K_l: 'L', pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O',
    pygame.K_p: 'P', pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
    pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X', pygame.K_y: 'Y',
    pygame.K_z: 'Z',
}


def hint_text_blit(width, height):
    hint_text = [
        'У вас есть 4 токена, 1 токен равня',
        'ется 5. Распределите все токены',
        'по характеристикам. Также дайте',
        'своему персонажу имя, Не превы',
        'шающее n символов.'
    ]

    with open('what_definition.txt', mode='r', encoding='utf-8') as file:
        if file.read() == '1920':
            k = 1
        else:
            k = 1.4055636896
        font2 = pygame.font.SysFont('candara', int(35 // k))

    text_coord = height // 15.8823529412 - 7
    for line in hint_text:
        string_rendered = font2.render(line, True, font_color2)
        intro_rect = string_rendered.get_rect()
        text_coord += 7
        intro_rect.top = text_coord
        intro_rect.x = width // 1.4479638009
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


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


def change_characteristics(symbol, parameter, character_id):
    global tokens, characteristics, img1, img2, img3, img4, font_color, font1

    connect = sqlite3.connect('game.db')
    cur = connect.cursor()

    if symbol == '+':
        tokens -= 5
        img_tokens = cur.execute(f'SELECT {parameter} FROM characteristics WHERE id = {character_id}').fetchone()
        cur.execute(f'UPDATE characteristics SET {parameter} = ? WHERE id = {character_id}',
                    (img_tokens[0] + 5,))
        characteristics[parameter] = font1.render(f'{img_tokens[0] + 5}', True, font_color)
    else:
        img_tokens = cur.execute(f'SELECT {parameter} FROM characteristics WHERE id = {character_id}').fetchone()
        if img_tokens[0] > 5:
            cur.execute(f'UPDATE characteristics SET {parameter} = ? WHERE id = {character_id}',
                        (img_tokens[0] - 5,))
            tokens += 5
            characteristics[parameter] = font1.render(f'{img_tokens[0] - 5}', True, font_color)

    img_tokens = cur.execute(f'SELECT {parameter} FROM characteristics WHERE id = {character_id}').fetchone()

    if parameter == 'strength':
        img1 = font1.render(f'{img_tokens[0]}', True, font_color)
    elif parameter == 'endurance':
        img2 = font1.render(f'{img_tokens[0]}', True, font_color)
    elif parameter == 'iq':
        img3 = font1.render(f'{img_tokens[0]}', True, font_color)
    else:
        img4 = font1.render(f'{img_tokens[0]}', True, font_color)

    connect.commit()
    cur.close()
    connect.close()


class BlackBackground(pygame.sprite.Sprite):
    image_black_background = pygame.Surface([719, 276])
    image_black_background.fill(pygame.Color("black"))

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(BlackBackground.image_black_background.get_width() / (2560 / width))
        image_height = round(BlackBackground.image_black_background.get_height() / (2560 / width))
        self.image = pygame.transform.scale(BlackBackground.image_black_background,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.45454545455
        self.rect.y = height // 16.6153846154

        self.image.set_alpha(220)


class EditorBack(pygame.sprite.Sprite):
    image_editor_back = load_image('pics/character_editor3.2.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(EditorBack.image_editor_back.get_width() / (2560 / width))
        image_height = round(EditorBack.image_editor_back.get_height() / (2560 / width))
        self.image = pygame.transform.scale(EditorBack.image_editor_back,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 3.09677419355
        self.rect.y = height // 18


class PlusButton(pygame.sprite.Sprite):
    image_plus_button = load_image('pics/plus_button.png')

    def __init__(self, width, height, position, characteristic, character_id, *groups):
        super().__init__(*groups)
        self.character_id = character_id
        image_width = round(PlusButton.image_plus_button.get_width() / (2560 / width))
        image_height = round(PlusButton.image_plus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(PlusButton.image_plus_button, (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.is_mouse_track = False
        self.characteristic = characteristic

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound2.play()
            if tokens > 0:
                change_characteristics('+', self.characteristic, self.character_id)
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class MinusButton(pygame.sprite.Sprite):
    image_minus_button = load_image('pics/minus_button.png')

    def __init__(self, width, height, position, characteristic, character_id, *groups):
        super().__init__(*groups)
        self.character_id = character_id
        image_width = round(MinusButton.image_minus_button.get_width() / (2560 / width))
        image_height = round(MinusButton.image_minus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(MinusButton.image_minus_button, (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.is_mouse_track = False
        self.characteristic = characteristic

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound2.play()
            if tokens < 20:
                change_characteristics('-', self.characteristic, self.character_id)
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class ContinueButton(pygame.sprite.Sprite):
    image_continue_button = load_image('pics/continue_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(ContinueButton.image_continue_button.get_width() / (2560 / width))
        image_height = round(ContinueButton.image_continue_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(ContinueButton.image_continue_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.74545454545
        self.rect.y = height // 1.12970711297
        self.is_mouse_track = False

    def update(self, *args):
        if tokens == 0 and is_enter is False and name != '':
            self.image.set_alpha(normal_alpha)
        else:
            self.image.set_alpha(disabled_alpha)
        if self.image.get_alpha() != disabled_alpha:
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


class CharacterNameEditorBack(pygame.sprite.Sprite):
    image_character_name_back = load_image('pics/character_name_back2.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(CharacterNameEditorBack.image_character_name_back.get_width() / (2560 / width))
        image_height = round(CharacterNameEditorBack.image_character_name_back.get_height() / (2560 / width))
        self.image = pygame.transform.scale(CharacterNameEditorBack.image_character_name_back,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 19.2
        self.rect.y = height // 18


class EnterButton(pygame.sprite.Sprite):
    image_enter_button = load_image('pics/enter_button2.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(EnterButton.image_enter_button.get_width() / (2560 / width))
        image_height = round(EnterButton.image_enter_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(EnterButton.image_enter_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 9.6
        self.rect.y = height // 3.08571428571
        self.is_mouse_track = False

    def update(self, *args):
        global is_enter
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            button_track_sound.play()
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            is_enter = True
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class SaveButton(pygame.sprite.Sprite):
    image_save_button = load_image('pics/save_button2.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(SaveButton.image_save_button.get_width() / (2560 / width))
        image_height = round(SaveButton.image_save_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(SaveButton.image_save_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 5.40845070423
        self.rect.y = height // 3.08571428571
        self.is_mouse_track = False

    def update(self, *args):
        global is_enter
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            button_track_sound.play()
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            is_enter = False
            connection = sqlite3.connect('game.db')
            cur = connection.cursor()
            cur.execute('''
                UPDATE characteristics
                SET name = ?
                WHERE id = (SELECT MAX(id) FROM characteristics)
            ''', (name,))

            connection.commit()
            cur.close()
            connection.close()

        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)

