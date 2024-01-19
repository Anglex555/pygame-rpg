import pygame
import sys

pygame.init()
with open('what_definition.txt', mode='r', encoding='utf-8') as file:
    width = int(file.read())
    height = (width // 16) * 9
screen = pygame.display.set_mode((width, height))
fps = 100
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def end_screen():
    pygame.init()

    background = pygame.Surface([1920, 1080])
    background.fill(pygame.Color("black"))
    background_width = round(background.get_width() / (2560 / width))
    background_height = round(background.get_height() / (2560 / width))
    background = pygame.transform.scale(background,
                                        (background_width, background_height))
    screen.blit(background, (0, 0))

    if width == 1920:
        k = 1
        y = 1080
    else:
        k = 1.4055636896
        y = 768
    font1 = pygame.font.SysFont('candara', int(35 // k), True)

    def blit_text(y):
        titles = [
            'Создатели:',
            'Александр Англичанинов',
            'Никита Анхимов',
            'Иван Седов',
            'Открытый мир -  Александр Англичанинов'
            'Город - Иван Седов'
            'Начальный и конечный экраны и главное меню - Никита Анхимов'
        ]
        text_coord = y - 7
        for line in titles:
            string_rendered = font1.render(line, True, 'white')
            intro_rect = string_rendered.get_rect()
            text_coord += 7
            intro_rect.top = text_coord
            intro_rect.x = 540
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    while True:
        if y == -273:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    return
        screen.blit(background, (0, 0))
        blit_text(y)
        y -= 1
        pygame.display.flip()
        clock.tick(fps)
