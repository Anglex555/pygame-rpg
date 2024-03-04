import os
import random

import pygame


pygame.init()
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
tile_width = tile_height = 100
with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    SCREEN_WIDTH = int(file.read())
    SCREEN_HEIGHT = (SCREEN_WIDTH // 16) * 9
size = SCREEN_WIDTH, SCREEN_HEIGHT
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('City')

k = 1 if SCREEN_WIDTH == 1366 else 1.4055636896

def profit(people, level, mnog):
    return people * level * mnog * 0.5


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


class House:
    def __init__(self, cord, level, human=None, color=None):
        super().__init__()
        self.level = level
        self.cord = cord
        self.human = human
        self.color = color
        self.clic = False

    def ret_color(self):
        return self.color

    def ret_human(self):
        return self.human

    def ret_level(self):
        return self.level

    def ret_cord(self):
        return self.cord

class Stat_up:
    def __init__(self, cord, level):
        self.cord = cord
        self.level = level
        self.stat_pount = 10
        self.name = 's1'
        self.form = [(self.cord), (self.cord[0], self.cord[1] + 1), (self.cord[0], self.cord[1] + 2)]
        self.img_viget = pygame.image.load("stat_viget.png")
        self.progruz = False
        self.clic = (0, 0)
        self.img_viget_x = pygame.image.load("viget_live2.png")
        self.img_viget_but = pygame.image.load("stat_button_buy.png")
        self.img_plus_yes = pygame.image.load("stat_button_plus_yes.png")
        self.img_plus_no = pygame.image.load("stat_button_plus_no.png")
        self.list_up = [20, 50, 10, 15, 20]
        self.list_up_stat = [[10, 20], [12, 30], [14, 40], [10, 15]]
        self.data_stat = [5, 3, 4, 5]

    def ret_list_up_stat(self):
        return self.list_up_stat

    def ret_stat_point(self):
        return self.stat_pount

    def red_stat_point(self, x):
        self.stat_pount = self.stat_pount + x

    def red_stat(self, i):
        self.data_stat[i] += 1


    def red_level(self, x):
        self.level = x

    def ret_v(self):
        return self.v

    def red_v(self, a):
        self.v = a

    def ret_form(self):
        return self.form

    def ret_name(self):
        return self.name

    def ret_clic(self):
        return self.clic

    def ret_exp(self):
        return 199999

    def ret_viget(self, sc):
        clic = self.clic
        lst_bust = ['Сила', 'Ловкость', 'Выносливость', 'Интелект']
        a = self.img_viget.get_rect(bottomright=clic)
        sc.blit(self.img_viget, a)
        x = self.img_viget_x.get_rect(bottomright=(clic[0], clic[1] - 340))
        sc.blit(self.img_viget_x, x)
        w = self.img_viget_but.get_rect(bottomright=clic)
        sc.blit(self.img_viget_but, w)
        q = 0
        f1 = pygame.font.Font(None, int(22))
        text2 = f1.render(f'Очков доступно: {self.stat_pount}', 1, (180, 0, 0))
        screen.blit(text2, (clic[0] - 150, clic[1] - 100))
        text3 = f1.render(f'Купить ещё за: \n{self.list_up_stat[self.level - 1][1]}дер.\n'
                          f' и {self.list_up_stat[self.level - 1][0]}exp', 1, (180, 0, 0))
        screen.blit(text3, (clic[0] - 150, clic[1] - 80))
        if self.stat_pount > 0:
            plus = self.img_plus_yes
        else:
            plus = self.img_plus_no
        for i in range(len(self.data_stat)):
            text1 = f1.render(f'{lst_bust[i]}', 1, (180, 0, 0))
            screen.blit(text1, (clic[0] - 330, clic[1] - 280 + q))
            pygame.draw.rect(screen, pygame.Color(25, 100, 0), (clic[0] - 330, clic[1] - 260 + q,
                                                                310 / sum(self.data_stat) * self.data_stat[i], 15))
            r = plus.get_rect(bottomright=(clic[0] - 20, clic[1] - 230 + q))
            sc.blit(plus, r)
            q += 40

    def ret_plus_but(self):
        if SCREEN_WIDTH == 1366:
            return [[range(1105, 1135), range(300, 330)], [range(1105, 1135), range(340, 370)],
                    [range(1105, 1135), range(380, 410)], [range(1105, 1135), range(420, 450)]]
        else:
            return [[range(1505, 1540), range(455, 485)], [range(1505, 1540), range(495, 525)],
                    [range(1505, 1540), range(535, 565)], [range(1505, 1540), range(575, 605)]]

    def progruz(self):
        return self.progruz

    def red_progruz(self, x):
        self.progruz = x

    def red_clic(self, clic):
        self.clic = clic

    def ret_range_viget(self):
        return (range(self.clic[0] - 350, self.clic[0]), range(self.clic[1] - 350, self.clic[1]))

    def red_count_viget(self, x):
        self.count_clic_viget = x

    def ret_range_x(self):
        return (range(self.clic[0] - 10, self.clic[0]), range(self.clic[1] - 350, self.clic[1] - 340))

    def ret_range_viget_but(self):
        return (range(self.clic[0] - 50, self.clic[0]), range(self.clic[1] - 50, self.clic[1]))

    def ret_list_up(self):
        return self.list_up

    def ret_cord(self):
        return self.cord


class Magaz:
    def __init__(self, cord, level):
        self.cord = cord
        self.level = level
        self.stat_pount = 1
        self.name = 'm1'
        self.form = [self.cord, (self.cord[0], self.cord[1] + 1), (self.cord[0] + 1, self.cord[1] + 1),
                     (self.cord[0] + 1, self.cord[1] + 2)]
        self.img_viget = pygame.image.load("viget_magaz.png")
        self.progruz = False
        self.clic = (0, 0)
        self.img_viget_x = pygame.image.load("viget_live2.png")
        self.img_viget_but = pygame.image.load("rerol.png")
        self.list_up = [20, 50, 10, 15, 20]
        self.list_up_stat = [[10, 20], [12, 30], [14, 40], [10, 15]]
        self.data_stat = [1, 1, 1, 1]
        self.tovar = self.ret_list_viget()

    def ret_list_viget(self):
        slovo_list = list('123456')
        abra = random.sample(slovo_list, len(slovo_list))
        return abra[:4]

    def rerol(self):
        self.tovar = self.ret_list_viget()

    def ret_list_up_stat(self):
        return self.list_up_stat

    def ret_stat_point(self):
        return self.stat_pount

    def red_stat_point(self, x):
        self.stat_pount = self.stat_pount + x

    def red_stat(self, i):
        self.tovar[i] = False


    def red_level(self, x):
        self.level = x

    def ret_v(self):
        return self.v

    def red_v(self, a):
        self.v = a

    def ret_form(self):
        return self.form

    def ret_name(self):
        return self.name

    def ret_clic(self):
        return self.clic

    def ret_exp(self):
        return 199999

    def ret_viget(self, sc):
        clic = self.clic
        a = self.img_viget.get_rect(bottomright=clic)
        sc.blit(self.img_viget, a)
        x = self.img_viget_x.get_rect(bottomright=(clic[0], clic[1] - 340))
        sc.blit(self.img_viget_x, x)
        w = self.img_viget_but.get_rect(bottomright=clic)
        sc.blit(self.img_viget_but, w)
        q = 0
        f1 = pygame.font.Font(None, int(22))
        text2 = f1.render(f'50 кам{" " * 9}50 кам{" " * 10}50 кам{" " * 11}50 кам', 1, (180, 0, 0))
        screen.blit(text2, (clic[0] - 330, clic[1] - 190))

        img_list = []
        for i in range(len(self.tovar)):
            if self.tovar[i]:
                img_list.append(pygame.image.load(f"tovar{self.tovar[i]}.png"))
            else:
                img_list.append(pygame.transform.scale(pygame.image.load("stat_button_plus_no.png"), (50, 50)))

        for i in range(0, 4):
            f = img_list[i].get_rect(bottomright=(clic[0] - 280 + q, clic[1] - 200))
            sc.blit(img_list[i], f)
            q += 87


    def ret_plus_but(self):
        if SCREEN_WIDTH == 1366:
            return [[range(825, 875), range(310, 360)], [range(910, 960), range(310, 360)],
                    [range(1000, 1050), range(310, 360)], [range(1085, 1135), range(310, 360)]]
        else:
            return [[range(1230, 1275), range(465, 515)], [range(1315, 1365), range(465, 515)],
                    [range(1405, 1450), range(465, 515)], [range(1490, 1540), range(465, 515)]]


    def progruz(self):
        return self.progruz

    def red_progruz(self, x):
        self.progruz = x

    def red_clic(self, clic):
        self.clic = clic

    def ret_range_viget(self):
        return (range(self.clic[0] - 350, self.clic[0]), range(self.clic[1] - 350, self.clic[1]))

    def red_count_viget(self, x):
        self.count_clic_viget = x

    def ret_range_x(self):
        return (range(self.clic[0] - 10, self.clic[0]), range(self.clic[1] - 350, self.clic[1] - 340))

    def ret_range_viget_but(self):
        return (range(self.clic[0] - 50, self.clic[0]), range(self.clic[1] - 50, self.clic[1]))

    def ret_list_up(self):
        return self.list_up

    def ret_cord(self):
        return self.cord




class Live(House):
    def __init__(self, cord, human, color, level):
        super().__init__(cord, human, color, level)
        self.name = 'l1'
        self.form = [(self.cord), (self.cord[0] - 1, self.cord[1]), (self.cord[0] - 2, self.cord[1])]
        self.img_viget = pygame.image.load("viget_live1.png")
        self.progruz = False
        self.clic = (0, 0)
        self.img_viget_x = pygame.image.load("viget_live2.png")
        self.img_viget_but = pygame.image.load("viget_live_but.png")
        self.list_up = [20, 50, 10, 15, 20]


    def red_level(self, x):
        self.level = x

    def ret_v(self):
        return self.v

    def red_v(self, a):
        self.v = a

    def ret_form(self):
        return self.form

    def ret_name(self):
        return self.name

    def ret_range_clic(self):
        return [[range(915, 1015), range(500, 550)], [range(915, 965), range(450, 500)]]

    def ret_clic(self):
        return self.clic

    def ret_viget(self, sc):
        clic = self.clic
        a = self.img_viget.get_rect(bottomright=clic)
        sc.blit(self.img_viget, a)
        x = self.img_viget_x.get_rect(bottomright=(clic[0], clic[1] - 60))
        sc.blit(self.img_viget_x, x)
        w = self.img_viget_but.get_rect(bottomright=clic)
        sc.blit(self.img_viget_but, w)
        f1 = pygame.font.Font(None, int(24 * k))
        text1 = f1.render(f' {self.level}', 1, (180, 0, 0))
        screen.blit(text1, (clic[0] - 65, clic[1] - 28))
        text2 = f1.render(f' {self.human * self.level}', 1, (180, 0, 0))
        screen.blit(text2, (clic[0] - 68, clic[1] - 45))
        f2 = pygame.font.Font(None, int(18 * k))
        if 0 <= self.level - 1 < len(self.list_up):
            text3 = f2.render(f'{self.list_up[self.level - 1]}', 1, (180, 0, 0))
            screen.blit(text3, (clic[0] - 30, clic[1] - 30))
        else:
            print("Недопустимый уровень для списка self.list_up")

    def progruz(self):
        return self.progruz

    def red_progruz(self, x):
        self.progruz = x

    def red_clic(self, clic):
        self.clic = clic

    def ret_range_viget(self):
        return (range(self.clic[0] - 120, self.clic[0]), range(self.clic[1] - 70, self.clic[1]))

    def red_count_viget(self, x):
        self.count_clic_viget = x

    def ret_range_x(self):
        return (range(self.clic[0] - 10, self.clic[0]), range(self.clic[1] - 70, self.clic[1] - 60))

    def ret_range_viget_but(self):
        return (range(self.clic[0] - 30, self.clic[0]), range(self.clic[1] - 15, self.clic[1]))

    def ret_list_up(self):
        return self.list_up


class Factory(House):
    def __init__(self, cord, human, color, level):
        super().__init__(cord, human, color, level)
        self.name = 'f1'
        self.max_people = self.level * 2
        self.form = [(self.cord), (self.cord[0] + 1, self.cord[1]), (self.cord[0] + 1, self.cord[1] - 1),
                     (self.cord[0], self.cord[1] - 1)]
        self.v = False
        self.img_viget = pygame.image.load("viget_fab1.png")
        self.img_viget_x = pygame.image.load("viget_live2.png")
        self.img_viget_but = pygame.image.load("viget_live_but.png")
        self.clic = (0, 0)
        self.list_up = [2, 50, 10, 15, 20]

    def red_level(self, x):
        self.level = x
        self.max_people = self.level * 3

    def red_progruz(self, x):
        self.progruz = x

    def ret_viget(self, sc):
        clic = self.clic
        a = self.img_viget.get_rect(bottomright=clic)
        sc.blit(self.img_viget, a)
        x = self.img_viget_x.get_rect(bottomright=(clic[0], clic[1] - 60))
        sc.blit(self.img_viget_x, x)
        sc.blit(self.img_viget_x, x)
        w = self.img_viget_but.get_rect(bottomright=clic)
        sc.blit(self.img_viget_but, w)
        f1 = pygame.font.Font(None, int(22 * k))
        text2 = f1.render(f' {self.level}', 1, (180, 0, 0))
        screen.blit(text2, (clic[0] - 68, clic[1] - 45))
        text1 = f1.render(f' {self.max_people}', 1, (180, 0, 0))
        screen.blit(text1, (clic[0] - 65, clic[1] - 28))
        text3 = f1.render(f' {self.ret_profit() * self.max_people}', 1, (180, 0, 0))
        screen.blit(text3, (clic[0] - 65, clic[1] - 15))
        f2 = pygame.font.Font(None, int(18 * k))
        if 0 <= self.level - 1 < len(self.list_up):
            text4 = f2.render(f'{self.list_up[self.level - 1]}', 1, (180, 0, 0))
            screen.blit(text4, (clic[0] - 30, clic[1] - 30))
        else:
            print("Недопустимый уровень для списка self.list_up")


    def ret_list_up(self):
        return self.list_up

    def progruz(self):
        return self.progruz

    def ret_v(self):
        return self.v

    def red_clic(self, clic):
        self.clic = clic

    def red_v(self, a):
        self.v = a

    def ret_count_clic_viget(self):
        return 0

    def ret_profit(self):
        return profit(self.human, self.level, 0.5)

    def ret_max_human(self):
        return self.max_people

    def plus_human(self, x, change=False):
        if change == -1:
            if self.human > 0:
                self.human = self.human - x
        else:
            if self.human < self.max_people:
                self.human = self.human + x

    def ret_form(self):
        return self.form

    def ret_name(self):
        return self.name

    def ret_range_clic(self):
        return [[range(915, 1015), range(500, 550)], [range(915, 965), range(450, 500)]]

    def ret_range_viget_but(self):
        return (range(self.clic[0] - 30, self.clic[0]), range(self.clic[1] - 15, self.clic[1]))

    def ret_range_viget(self):
        return (range(self.clic[0] - 120, self.clic[0]), range(self.clic[1] - 70, self.clic[1]))

    def ret_range_x(self):
        return (range(self.clic[0] - 10, self.clic[0]), range(self.clic[1] - 70, self.clic[1] - 60))


class Factory_s(House):
    def __init__(self, cord, human, color, level):
        super().__init__(cord, human, color, level)
        self.name = 'f2'
        self.max_people = self.level * 2
        self.form = [(self.cord), (self.cord[0] + 1, self.cord[1]), (self.cord[0] + 1, self.cord[1] - 1),
                     (self.cord[0], self.cord[1] - 1)]
        self.v = False
        self.img_viget = pygame.image.load("viget_fab1.png")
        self.img_viget_x = pygame.image.load("viget_live2.png")
        self.img_viget_but = pygame.image.load("viget_live_but.png")
        self.clic = (0, 0)
        self.list_up = [2, 50, 10, 15, 20]

    def red_level(self, x):
        self.level = x
        self.max_people = self.level * 3

    def red_progruz(self, x):
        self.progruz = x

    def ret_viget(self, sc):
        clic = self.clic
        a = self.img_viget.get_rect(bottomright=clic)
        sc.blit(self.img_viget, a)
        x = self.img_viget_x.get_rect(bottomright=(clic[0], clic[1] - 60))
        sc.blit(self.img_viget_x, x)
        sc.blit(self.img_viget_x, x)
        w = self.img_viget_but.get_rect(bottomright=clic)
        sc.blit(self.img_viget_but, w)
        f1 = pygame.font.Font(None, int(22 * k))
        text2 = f1.render(f' {self.level}', 1, (180, 0, 0))
        screen.blit(text2, (clic[0] - 68, clic[1] - 45))
        text1 = f1.render(f' {self.max_people}', 1, (180, 0, 0))
        screen.blit(text1, (clic[0] - 65, clic[1] - 28))
        text3 = f1.render(f' {self.ret_profit() * self.max_people}', 1, (180, 0, 0))
        screen.blit(text3, (clic[0] - 65, clic[1] - 15))
        f2 = pygame.font.Font(None, int(18 * k))
        if 0 <= self.level - 1 < len(self.list_up):
            text4 = f2.render(f'{self.list_up[self.level - 1]}', 1, (180, 0, 0))
            screen.blit(text4, (clic[0] - 30, clic[1] - 30))
        else:
            print('Ошибка: недопустимый индекс для списка self.list_up')

    def ret_list_up(self):
        return self.list_up

    def progruz(self):
        return self.progruz

    def ret_v(self):
        return self.v

    def red_clic(self, clic):
        self.clic = clic

    def red_v(self, a):
        self.v = a

    def ret_count_clic_viget(self):
        return 0

    def ret_profit(self):
        return profit(self.human, self.level, 0.5)

    def ret_max_human(self):
        return self.max_people

    def plus_human_(self, x, change=False):
        if change == -1:
            if self.human > 0:
                self.human = self.human - x
        else:
            if self.human < self.max_people:
                self.human = self.human + x

    def ret_form(self):
        return self.form

    def ret_name(self):
        return self.name

    def ret_range_clic(self):
        return [[range(915, 1015), range(500, 550)], [range(915, 965), range(450, 500)]]

    def ret_range_viget_but(self):
        return (range(self.clic[0] - 30, self.clic[0]), range(self.clic[1] - 15, self.clic[1]))

    def ret_range_viget(self):
        return (range(self.clic[0] - 120, self.clic[0]), range(self.clic[1] - 70, self.clic[1]))

    def ret_range_x(self):
        return (range(self.clic[0] - 10, self.clic[0]), range(self.clic[1] - 70, self.clic[1] - 60))


class City_desk:
    def __init__(self, name, list_house):
        super(City_desk, self).__init__()
        self.name = name
        self.list_house = list_house

    def ret_name(self):
        return self.name

    def ret_listhouse(self):
        return self.list_house

    def ret_people(self, name, plus=False, change=False):
        rezl1 = 0
        rezf1 = 0
        rezf2 = 0
        for i in range(len(self.list_house)):
            if self.list_house[i].ret_name() == 'l1':
                rezl1 += self.list_house[i].ret_human() * self.list_house[i].ret_level()

            elif self.list_house[i].ret_name() == 'f1':
                rezf1 += self.list_house[i].ret_human()

            elif self.list_house[i].ret_name() == 'f2':
                rezf2 += self.list_house[i].ret_human()
        if plus:
            if name == 'f1':
                for i in range(len(self.list_house)):
                    if self.list_house[i].ret_name() == 'f1':
                        if change:

                            if change == -1 and 0 <= rezl1 - (rezf1 + rezf2):
                                self.list_house[i].plus_human(1, change)
                            if change == 1 and rezl1 > rezf1 + rezf2:
                                self.list_house[i].plus_human(1, change)

            if name == 'f2':
                for i in range(len(self.list_house)):
                    if self.list_house[i].ret_name() == 'f2':
                        if change:
                            if change == -1 and 0 <= rezl1 - (rezf1 + rezf2):
                                self.list_house[i].plus_human_(1, change)
                            if change == 1 and rezl1 > rezf1 + rezf2:
                                self.list_house[i].plus_human_(1, change)
        else:
            if name == 'l1':
                return rezl1

            elif name == 'f1':
                return rezf1

            elif name == 'f2':
                return rezf2

            elif name == 'f':
                return rezf1 + rezf2

    def ret_max_people(self, name):
        rez1 = 0
        rez2 = 0
        if name == 'f1':
            for i in range(len(self.list_house)):
                if self.list_house[i].ret_name() == 'f1':
                    rez1 += self.list_house[i].ret_max_human()
            return rez1
        elif name == 'f2':
            for i in range(len(self.list_house)):
                if self.list_house[i].ret_name() == 'f2':
                    rez2 += self.list_house[i].ret_max_human()
            return rez2


class Button:
    def __init__(self, name, cord, size):
        super(Button, self).__init__()
        self.name = name
        self.cord = cord
        self.size = size

    def ret_cord(self):
        return self.cord

    def ret_name(self):
        return self.name


lst_button = [Button('+', (200, 330), (40, 40)), Button('-', (50, 330), (40, 40)),
              Button('+', (200, 530), (40, 40)), Button('-', (50, 530), (40, 40))]


class Board:
    def __init__(self, width, height, city, lst_butt):
        self.stok2 = 5
        self.lst_butt = lst_butt
        self.a = 0
        self.stok1 = 10
        self.city = city
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.colors = [pygame.Color(0, 0, 0), pygame.Color(255, 0, 0), pygame.Color(0, 0, 255)]
        self.current_color = 0
        self.list_house = city.ret_listhouse()
        self.fps = 0
        self.count_clic = False
        self.f = True
        self.rez1 = 0


    def render(self, city):
        if self.fps == 60000:
            self.fps = 0
        self.fps += 1

        f1 = pygame.font.Font(None, int(36 * k))
        text1 = f1.render(f'Название: {self.city.ret_name()}', 1, (180, 0, 0))
        screen.blit(text1, (int(50 * k), int(30 * k)))

        text2 = f1.render(f'Все жители: {self.city.ret_people("l1")}', 1, (180, 0, 0))
        screen.blit(text2, (int(50 * k), int(80 * k)))

        text4 = f1.render(f'Незанятые жители: {self.city.ret_people("l1") - self.city.ret_people("f")}', 1,
                          (180, 0, 0))
        screen.blit(text4, (int(50 * k), int(130 * k)))
        self.rez1 = 0
        self.rez2 = 0
        for i in range(len(self.list_house)):
            if self.list_house[i].ret_name() == 'f1':
                self.rez1 += self.list_house[i].ret_profit()

        for i in range(len(self.list_house)):
            if self.list_house[i].ret_name() == 'f2':
                self.rez2 += self.list_house[i].ret_profit()

        self.a += 1
        if self.a % 60 == 0:
            self.stok1 += self.rez1
            self.stok2 += self.rez2

        text3 = f1.render(f'Дерево +{self.rez1}: {self.stok1}', 1, (180, 0, 0))
        screen.blit(text3, (int(50 * k), int(180 * k)))

        text5 = f1.render(f'Эффективность: {int(self.city.ret_people("f1") * 100 / self.city.ret_max_people("f1"))}%', 1,
                          (180, 0, 0))
        screen.blit(text5, (int(50 * k), int(230 * k)))

        q = 400 // city.ret_max_people("f1")
        for i in range(city.ret_max_people("f1")):
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), (int(50 + q * i * k), int(280 * k), int(400 // city.ret_max_people("f1") * k) + 1, int(30 * k)), 1)

        q = 400 // city.ret_max_people("f1")

        for i in range(self.city.ret_people("f1")):
            pygame.draw.rect(screen, pygame.Color(25, 100, 0), (int(50 + q * i * k), int(280 * k), int(400 // city.ret_max_people("f1") * k) + 1, int(30 * k)))


        text6 = f1.render(f'Камень +{self.rez2}: {self.stok2}', 1, (180, 0, 0))
        screen.blit(text6, (int(50 * k), int(380 * k)))

        text7 = f1.render(f'Эффективность: {int(self.city.ret_people("f2") * 100 / self.city.ret_max_people("f2"))}%', 1,
                          (180, 0, 0))
        screen.blit(text7, (int(50 * k), int(430 * k)))

        q = 400 // city.ret_max_people("f2")
        for i in range(city.ret_max_people("f2")):
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), (int(50 + q * i * k), int(480 * k), int(400 // city.ret_max_people("f2") * k) + 1, int(30 * k)), 1)

        q = 400 // city.ret_max_people("f2")

        for i in range(self.city.ret_people("f2")):
            pygame.draw.rect(screen, pygame.Color(25, 100, 150), (int(50 + q * i * k), int(480 * k), int(400 // city.ret_max_people("f2") * k) + 1, int(30 * k)))

        for i in range(len(self.list_house)):
            if self.list_house[i].progruz:
                self.list_house[i].ret_viget(screen)



    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell, qx, qy):
        if self.count_clic and (self.count_clic in range(self.fps - 10, self.fps)):
            print(2)

        if cell[0] in range(int(805 * k), int(1165 * k)) and cell[1] in range(int(210 * k), int(560 * k)):
            x, y = cell[0] - int(self.left * k), cell[1] - int(self.top * k)
            row, col = int(y // (self.cell_size * k)), int(x // (self.cell_size * k))
            if 0 <= row < self.height and 0 <= col < self.width:
                self.board[row][col] = (self.board[row][col] + 1) % 3
            else:
                print("Некорректные координаты ячейки")

            for i in range(len(self.list_house)):
                if str((col, row)) in str(self.list_house[i].ret_form()) and self.f:
                    self.f = False
                    self.list_house[i].red_progruz(True)
                    print(1)
                    if self.list_house[i].ret_name() == 's1' or self.list_house[i].ret_name() == 'm1':
                        self.list_house[i].red_clic((int(1155 * k) - 65, int(560 * k) - 70))
                    else:
                        self.list_house[i].red_clic((cell[0], cell[1]))

                if cell[0] in self.list_house[i].ret_range_viget()[0] \
                        and cell[1] in self.list_house[i].ret_range_viget()[1]:
                    if cell[0] in self.list_house[i].ret_range_x()[0] \
                            and cell[1] in self.list_house[i].ret_range_x()[1]:
                        print(12)
                        self.f = True
                        self.list_house[i].red_progruz(False)

                    if cell[0] in self.list_house[i].ret_range_viget_but()[0] \
                            and cell[1] in self.list_house[i].ret_range_viget_but()[1]:

                        if self.list_house[i].ret_name() == 's1' \
                                and self.stok1 >= self.list_house[i].ret_list_up_stat()[1][1]:
                            z = self.list_house[i].ret_list_up_stat()[1][1]
                            self.stok1 = self.stok1 - z
                            self.list_house[i].red_stat_point(1)

                        elif self.list_house[i].ret_name() == 'm1':
                            self.list_house[i].rerol()

                        elif self.list_house[i].ret_name() != 's1':
                            if 0 <= self.list_house[i].ret_level() - 1 < len(self.list_house[i].ret_list_up()):
                                # Индекс находится в допустимом диапазоне
                                if self.stok1 >= self.list_house[i].ret_list_up()[self.list_house[i].ret_level() - 1]:
                                    z = self.list_house[i].ret_list_up()[self.list_house[i].ret_level() - 1]
                                    self.stok1 = self.stok1 - z
                                    self.list_house[i].red_level(self.list_house[i].ret_level() + 1)
                                else:
                                    print('Error: нет денег')
                            else:
                                print('Ошибка: Недопустимый уровень для списка self.list_up')

                    elif self.list_house[i].ret_name() == 's1':
                        for j in range(len(self.list_house[i].ret_plus_but())):
                            if cell[0] in self.list_house[i].ret_plus_but()[j][0] \
                                    and cell[1] in self.list_house[i].ret_plus_but()[j][1]:

                                if self.list_house[i].ret_stat_point() > 0:
                                    print(7878)
                                    self.list_house[i].red_stat(j)
                                    self.list_house[i].red_stat_point(-1)
                                else:
                                    print('нет поинтов')

                    elif self.list_house[i].ret_name() == 'm1':
                        for j in range(len(self.list_house[i].ret_plus_but())):
                            print(cell[0], "===", self.list_house[i].ret_plus_but()[j][0])
                            print(cell[1], "=!=!=",self.list_house[i].ret_plus_but()[j][1])
                            if cell[0] in self.list_house[i].ret_plus_but()[j][0] \
                                    and cell[1] in self.list_house[i].ret_plus_but()[j][1]:
                                if self.stok2 - 50 >= 0:
                                    self.stok2 = self.stok2 - 50
                                    print(j)
                                    self.list_house[i].red_stat(j)
                                else:
                                    print('нет поинтов')

        elif cell[0] in range(int(200 * k), int(240 * k)) and cell[1] in range(int(330 * k), int(370 * k)):
            if 0 < self.city.ret_people("l1") - self.city.ret_people("f1"):
                self.city.ret_people('f1', True, 1)
                print(1)

        elif cell[0] in range(int(50 * k), int(90 * k)) and cell[1] in range(int(330 * k), int(370 * k)):
            self.city.ret_people('f1', True, -1)
            print(2)

        elif cell[0] in range(int(200 * k), int(240 * k)) and cell[1] in range(int(530 * k), int(570 * k)):
            if 0 < self.city.ret_people("l1") - self.city.ret_people("f2"):
                self.city.ret_people('f2', True, 1)

        elif cell[0] in range(int(50 * k), int(90 * k)) and cell[1] in range(int(530 * k), int(570 * k)):
            self.city.ret_people('f2', True, -1)


def run_game():
    pygame.init()
    x_p = 805
    y_p = 210
    house = [Stat_up((1, 4), 1), Live((6, 6), 3, 2, 1), Factory((4, 2), 2, 1, 2), Magaz((0, 0), 1),
            Factory_s((3, 4), 2, 3, 3)]
    city = City_desk('Vanyalend', house)
    board = Board(7, 7, city, lst_button)
    board.set_view(805, 210, 50)
    all_sprites = pygame.sprite.Group()

    sprite_pole = pygame.sprite.Sprite()
    sprite_pole.image = pygame.transform.scale(pygame.image.load("town_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    sprite_pole.rect = sprite_pole.image.get_rect()
    all_sprites.add(sprite_pole)
    sprite_pole.rect.x = 0
    sprite_pole.rect.y = 0

    q = 0
    for i in range(2):
        sprite_plus = pygame.sprite.Sprite()
        sprite_plus.image = pygame.transform.scale(pygame.image.load("but_plus.png"), (int(40 * k), int(40 * k)))
        sprite_plus.rect = sprite_plus.image.get_rect()
        all_sprites.add(sprite_plus)
        sprite_plus.rect.x = int(200 * k)
        sprite_plus.rect.y = int((330 + q) * k)
        q += 200
    q = 0
    for i in range(2):
        sprite_minus = pygame.sprite.Sprite()
        sprite_minus.image = pygame.transform.scale(pygame.image.load("but_minus.png"), (int(40 * k), int(40 * k)))
        sprite_minus.rect = sprite_minus.image.get_rect()
        all_sprites.add(sprite_minus)
        sprite_minus.rect.x = int(50 * k)
        sprite_minus.rect.y = int((330 + q) * k)
        q += 200

    qx = 325 if SCREEN_WIDTH == 1920 else 0
    qy = 85 if SCREEN_WIDTH == 1920 else 0

    sprite_fab_tree = pygame.sprite.Sprite()
    sprite_fab_tree.image = pygame.transform.scale(pygame.image.load("production_tree.png"), (int(100 * k), int(100 * k)))
    sprite_fab_tree.rect = sprite_fab_tree.image.get_rect()
    all_sprites.add(sprite_fab_tree)
    s = house[2].ret_cord()
    sprite_fab_tree.rect.x = x_p + k * 50 * s[0] + qx
    sprite_fab_tree.rect.y = y_p + k * 50 * (s[1] - 1) + qy

    s = house[0].ret_cord()
    sprite_stat = pygame.sprite.Sprite()
    sprite_stat.image = scale = pygame.transform.scale(pygame.image.load("upgrade.png"), (int(50 * k), int(150 * k)))
    sprite_stat.rect = sprite_stat.image.get_rect()
    all_sprites.add(sprite_stat)
    sprite_stat.rect.x = x_p + k * 50 * s[0] + qx
    sprite_stat.rect.y = y_p + k * 50 * s[1] + qy

    s = house[1].ret_cord()
    sprite_live = pygame.sprite.Sprite()
    sprite_live.image = pygame.transform.scale(pygame.image.load("dwelling.png"), (int(150 * k), int(50 * k)))
    sprite_live.rect = sprite_live.image.get_rect()
    all_sprites.add(sprite_live)
    sprite_live.rect.x = x_p + k * 50 * (s[0] - 2) + qx
    sprite_live.rect.y = y_p + k * 50 * s[1] + qy

    s = house[3].ret_cord()
    sprite_magaz = pygame.sprite.Sprite()
    sprite_magaz.image = pygame.transform.scale(pygame.image.load("market.png"), (int(100 * k), int(150 * k)))
    sprite_magaz.rect = sprite_magaz.image.get_rect()
    all_sprites.add(sprite_magaz)
    sprite_magaz.rect.x = x_p + k * 50 * s[0] + qx
    sprite_magaz.rect.y = y_p + k * 50 * s[1] + qy

    s = house[-1].ret_cord()
    sprite_stoune = pygame.sprite.Sprite()
    sprite_stoune.image = pygame.transform.scale(pygame.image.load("production_stone.png"), (int(100 * k), int(100 * k)))
    sprite_stoune.rect = sprite_magaz.image.get_rect()
    all_sprites.add(sprite_stoune)
    sprite_stoune.rect.x = x_p + k * 50 * s[0] + qx
    sprite_stoune.rect.y = y_p + k * 51 * s[1] + qy

    running = True
    dog_surf = pygame.image.load('but_plus.png')
    dog_rect = dog_surf.get_rect(bottomright=(0, 0))
    screen.blit(dog_surf, dog_rect)
    pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_g:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.on_click(event.pos, qx, qy)
        clock.tick(FPS)
        all_sprites.draw(screen)
        board.render(city)
        pygame.display.flip()
