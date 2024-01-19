import pygame
import os

# Добавление интерфейса
uf_bg_simple = pygame.transform.scale(pygame.image.load(os.path.join("data", "uf_bg_simple.png")), (409, 134))
uf_bg_halfelite = pygame.transform.scale(pygame.image.load(os.path.join("data", "uf_bg_halfelite.png")), (448, 140))
uf_bg_elite = pygame.transform.scale(pygame.image.load(os.path.join("data", "uf_bg_elite.png")), (448, 140))
uf_bar_b_health = pygame.transform.scale(pygame.image.load(os.path.join("data", "uf_bar_b_health.png")), (260, 28))
uf_bar_sm_mana = pygame.transform.scale(pygame.image.load(os.path.join("data", "uf_bar_sm_mana.png")), (210, 38))

# Функция для отображения интерфейса
def draw_interface(screen, hero):
    # Отображение фона интерфейса в левом верхнем углу
    interface_bg = uf_bg_simple
    if hero.lvl >= 5:
        interface_bg = uf_bg_halfelite
    if hero.lvl >= 10:
        interface_bg = uf_bg_elite
    screen.blit(interface_bg, (10, 10))

    # Отображение уровня игрока и прогресса опыта
    font = pygame.font.Font(None, 90)
    level_text = font.render(f"{hero.lvl}", True, (255, 255, 255))
    font = pygame.font.Font(None, 30)
    exp_percentage = (hero.exp / hero.exp_levelup) * 100
    exp_text = font.render(f"{exp_percentage:.2f}%", True, (255, 255, 255))

    # Расположение текста на интерфейсе
    if hero.lvl >= 10:
        screen.blit(level_text, (84, 43))
        screen.blit(exp_text, (84, 100))
    elif hero.lvl >= 5:
        screen.blit(level_text, (99, 43))
        screen.blit(exp_text, (84, 100))
    else:
        screen.blit(level_text, (60, 35))
        screen.blit(exp_text, (45, 92))

    # Отображение полосы здоровья
    hp_percentage = (hero.hp / hero.max_hp) * 100
    hpbar_width = int(230 * (hp_percentage / 100))
    hpbar_rect = pygame.Rect(36, 16, hpbar_width, 20)
    screen.blit(uf_bar_b_health, (145, 60), hpbar_rect)

    mana_percentage = (hero.mana / hero.max_mana) * 100
    manabar_width = int(170 * (mana_percentage / 100))
    manabar_rect = pygame.Rect(36, 16, manabar_width, 20)
    screen.blit(uf_bar_sm_mana, (145, 81), manabar_rect)

