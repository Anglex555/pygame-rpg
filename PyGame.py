import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = pygame.Surface([20, 20])
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(x, y, 20, 20)

    def reset_position(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)

    def move(self, m):
        self.rect = self.rect.move(m, 0)

    def move_vertically(self, m):
        self.rect = self.rect.move(0, m)

    def update(self):
        if not pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(0, 1)


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(vertical_borders)
        self.image = pygame.Surface([10, 50])
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(x, y, 10, 50)


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(vertical_borders)
        self.image = pygame.Surface([50, 10])
        self.image.fill((125, 125, 125))
        self.rect = pygame.Rect(x, y, 50, 10)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лесенки')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    running = True
    all_sprites = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    clock = pygame.time.Clock()
    ball_created = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    Ladder(event.pos[0], event.pos[1])
                elif event.button == 1:
                    Border(event.pos[0], event.pos[1])
                elif event.button == 3:
                    if not ball_created:
                        ball = Ball(event.pos[0], event.pos[1])
                        ball_created = True
                    else:
                        ball.reset_position(event.pos[0], event.pos[1])
                        
        keys = pygame.key.get_pressed()
        if ball_created and pygame.sprite.spritecollideany(ball, vertical_borders):
            if keys[pygame.K_RIGHT]:
                ball.move(10)
            elif keys[pygame.K_LEFT]:
                ball.move(-10)
            elif keys[pygame.K_UP]:
                ball.move_vertically(-10)
            elif keys[pygame.K_DOWN]:
                ball.move_vertically(10)

        all_sprites.update()
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(20)
