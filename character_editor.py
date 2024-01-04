import pygame
import sys
import os
import sqlite3


pygame.init()
with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    width = int(file.read())
    height = (width // 16) * 9
button_sound = pygame.mixer.Sound('sound_effects/button_click_4.mp3')
button_track_sound = pygame.mixer.Sound('sound_effects/button_tracking_04.mp3')
main_menu_music = pygame.mixer.Sound('music/main_menu_music.mp3')
screen = pygame.display.set_mode((width, height))
normal_alpha = 255
hover_alpha = 215
pressed_alpha = 150
disabled_alpha = 100
font_color = (196, 183, 166)
tokens = 20
token = 5
font1 = pygame.font.SysFont('candara', 50)
img1 = font1.render('5', True, font_color)
img2 = font1.render('5', True, font_color)
img3 = font1.render('5', True, font_color)
img4 = font1.render('5', True, font_color)

characteristics = {'strength': img1, 'endurance': img2, 'iq': img3, 'body_type': img4}


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


def change_characteristics(symbol, parameter):
    global tokens, characteristics, img1, img2, img3, img4, font_color, font1

    connect = sqlite3.connect('game.db')
    cur = connect.cursor()

    if symbol == '+':
        tokens -= token
        if parameter == 'strength':
            img_tokens = cur.execute('''
                SELECT strength FROM characteristics
                WHERE id = 1
            ''').fetchone()
            cur.execute('''
                UPDATE characteristics
                SET strength = ?
                WHERE id = 1
            ''', (str(img_tokens[0] + token),))
            img1 = font1.render(f'{img_tokens[0] + token}', True, font_color)
        elif parameter == 'endurance':
            img_tokens = cur.execute('''
                SELECT endurance FROM characteristics
                WHERE id = 1
            ''').fetchone()
            cur.execute('''
                UPDATE characteristics
                SET endurance = ?
                WHERE id = 1
            ''', (str(img_tokens[0] + token),))
            img2 = font1.render(f'{img_tokens[0] + token}', True, font_color)
        elif parameter == 'iq':
            img_tokens = cur.execute('''
                SELECT iq FROM characteristics
                WHERE id = 1
            ''').fetchone()
            cur.execute('''
                UPDATE characteristics
                SET iq = ?
                WHERE id = 1
            ''', (str(img_tokens[0] + token),))
            img3 = font1.render(f'{img_tokens[0] + token}', True, font_color)
        else:
            img_tokens = cur.execute('''
                SELECT body_type FROM characteristics
                WHERE id = 1
            ''').fetchone()
            cur.execute('''
                UPDATE characteristics
                SET body_type = ?
                WHERE id = 1
            ''', (str(img_tokens[0] + token),))
            img4 = font1.render(f'{img_tokens[0] + token}', True, font_color)

    else:
        if parameter == 'strength':
            img_tokens = cur.execute('''
                SELECT strength FROM characteristics
                WHERE id = 1
            ''').fetchone()
            if img_tokens[0] > 5:
                cur.execute('''
                    UPDATE characteristics
                    SET strength = ?
                    WHERE id = 1
                ''', (str(img_tokens[0] - token),))
                tokens += token
                img1 = font1.render(f'{img_tokens[0] - token}', True, font_color)
        elif parameter == 'endurance':
            img_tokens = cur.execute('''
                SELECT endurance FROM characteristics
                WHERE id = 1
            ''').fetchone()
            if img_tokens[0] > 5:
                cur.execute('''
                    UPDATE characteristics
                    SET endurance = ?
                    WHERE id = 1
                ''', (str(img_tokens[0] - token),))
                tokens += token
                img2 = font1.render(f'{img_tokens[0] - token}', True, font_color)
        elif parameter == 'iq':
            img_tokens = cur.execute('''
                SELECT iq FROM characteristics
                WHERE id = 1
            ''').fetchone()
            if img_tokens[0] > 5:
                cur.execute('''
                    UPDATE characteristics
                    SET iq = ?
                    WHERE id = 1
                ''', (str(img_tokens[0] - token),))
                tokens += token
                img3 = font1.render(f'{img_tokens[0] - token}', True, font_color)
        else:
            img_tokens = cur.execute('''
                SELECT body_type FROM characteristics
                WHERE id = 1
            ''').fetchone()
            if img_tokens[0] > 5:
                cur.execute('''
                    UPDATE characteristics
                    SET body_type = ?
                    WHERE id = 1
                ''', (str(img_tokens[0] - token),))
                tokens += token
                img4 = font1.render(f'{img_tokens[0] - token}', True, font_color)

    connect.commit()
    cur.close()
    connect.close()


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


class PlusButton1(pygame.sprite.Sprite):
    image_plus_button = load_image('pics/plus_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(PlusButton1.image_plus_button.get_width() / (2560 / width))
        image_height = round(PlusButton1.image_plus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(PlusButton1.image_plus_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.66956521739
        self.rect.y = height // 1.66666666667
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            if tokens > 0:
                change_characteristics('+', 'strength')
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class MinusButton1(pygame.sprite.Sprite):
    image_minus_button = load_image('pics/minus_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(MinusButton1.image_minus_button.get_width() / (2560 / width))
        image_height = round(MinusButton1.image_minus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(MinusButton1.image_minus_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.72972972973
        self.rect.y = height // 1.66666666667
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            if tokens < 20:
                change_characteristics('-', 'strength')
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class PlusButton2(pygame.sprite.Sprite):
    image_plus_button = load_image('pics/plus_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(PlusButton2.image_plus_button.get_width() / (2560 / width))
        image_height = round(PlusButton2.image_plus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(PlusButton2.image_plus_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.66956521739
        self.rect.y = height // 1.50627615063
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            if tokens > 0:
                change_characteristics('+', 'endurance')
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class MinusButton2(pygame.sprite.Sprite):
    image_minus_button = load_image('pics/minus_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(MinusButton2.image_minus_button.get_width() / (2560 / width))
        image_height = round(MinusButton2.image_minus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(MinusButton2.image_minus_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.72972972973
        self.rect.y = height // 1.50627615063
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            if tokens < 20:
                change_characteristics('-', 'endurance')
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class PlusButton3(pygame.sprite.Sprite):
    image_plus_button = load_image('pics/plus_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(PlusButton3.image_plus_button.get_width() / (2560 / width))
        image_height = round(PlusButton3.image_plus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(PlusButton3.image_plus_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.66956521739
        self.rect.y = height // 1.37404580153
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            if tokens > 0:
                change_characteristics('+', 'iq')
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class MinusButton3(pygame.sprite.Sprite):
    image_minus_button = load_image('pics/minus_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(MinusButton3.image_minus_button.get_width() / (2560 / width))
        image_height = round(MinusButton3.image_minus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(MinusButton3.image_minus_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.72972972973
        self.rect.y = height // 1.37404580153
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            if tokens < 20:
                change_characteristics('-', 'iq')
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class PlusButton4(pygame.sprite.Sprite):
    image_plus_button = load_image('pics/plus_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(PlusButton4.image_plus_button.get_width() / (2560 / width))
        image_height = round(PlusButton4.image_plus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(PlusButton4.image_plus_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.66956521739
        self.rect.y = height // 1.26315789474
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            if tokens > 0:
                change_characteristics('+', 'body_type')
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)


class MinusButton4(pygame.sprite.Sprite):
    image_minus_button = load_image('pics/minus_button.png')

    def __init__(self, width, height, *group):
        super().__init__(*group)
        image_width = round(MinusButton4.image_minus_button.get_width() / (2560 / width))
        image_height = round(MinusButton4.image_minus_button.get_height() / (2560 / width))
        self.image = pygame.transform.scale(MinusButton4.image_minus_button,
                                            (image_width, image_height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 1.72972972973
        self.rect.y = height // 1.26315789474
        self.is_mouse_track = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos) and self.is_mouse_track is False:
            self.image.set_alpha(hover_alpha)
            self.is_mouse_track = True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(pressed_alpha)
            button_sound.play()
            if tokens < 20:
                change_characteristics('-', 'body_type')
        if args and args[0].type == pygame.MOUSEBUTTONUP and \
                self.rect.collidepoint(args[0].pos):
            self.image.set_alpha(hover_alpha)
        elif args and args[0].type == pygame.MOUSEMOTION and \
                not self.rect.collidepoint(args[0].pos):
            self.is_mouse_track = False
            self.image.set_alpha(normal_alpha)