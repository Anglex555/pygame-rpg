import pygame
import sys

pygame.init()
with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    width = int(file.read())
    height = (width // 16) * 9
screen = pygame.display.set_mode((width, height))
fps = 200
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.init()

    background = pygame.image.load('pics/rpg_background_start_screen3.png')
    background_width = round(background.get_width() / (2560 / width))
    background_height = round(background.get_height() / (2560 / width))
    background = pygame.transform.scale(background,
                                        (background_width, background_height))
    background.set_alpha(200)
    screen.blit(background, (0, 0))

    if width == 1920:
        k = 1
        y = 1080
    else:
        k = 1.4055636896
        y = 768
    font1 = pygame.font.SysFont('candara', int(35 // k), True)
    font2 = pygame.font.SysFont('comicsansms', int(20 // k))
    continue_text = font2.render('Нажмите x чтобы продолжить ', True, 'orange')

    def blit_text(y):
        intro_text = [
            'События происходят на острове [пока не придумали],',
            'вы играете за персонажа, который приехал на этот',
            'остров, потому что [еще не придумали].',
            '',
            'В начале игры вы сможете настроить своего персона',
            'жа, увеличив определенные характеристики, в которые',
            'входит сила, выносливость, интеллект и телосложение.',
            'Так же вы сможете дать имя вашему персонажу.',
            '',
            'В игре вы будете путешествовать по острову,',
            'попутно открывая новые земли и города, сражаться с',
            'монстрами, с которых вы будете получать опыт, взаимо',
            'действовать с жителями городов и деревень, исследо',
            'вать подземелья, прокачивать оружие и развивать свой город.',
            'В городе вы должны будете добывать ресурсы, распределять',
            'жителей по предприятиям, прокачивать здания. В гильдии вам',
            'будут доступны задания, за которыые вы будете получать опыт.'
        ]
        text_coord = y - 7
        for line in intro_text:
            string_rendered = font1.render(line, True, 'white')
            intro_rect = string_rendered.get_rect()
            text_coord += 7
            intro_rect.top = text_coord
            intro_rect.x = width // 3.55555555556
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    while True:
        if (y == -680 and width == 1920) or (y == -505 and width == 1366):
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    return
        screen.blit(background, (0, 0))
        screen.blit(continue_text, (width // 96, height // 1.03846153846))
        blit_text(y)
        y -= 1
        pygame.display.flip()
        clock.tick(fps)

