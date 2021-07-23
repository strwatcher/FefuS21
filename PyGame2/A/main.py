import random

import pygame as pg

pg.init()
horizontal_borders = pg.sprite.Group()
vertical_borders = pg.sprite.Group()
balls = pg.sprite.Group()


class Ball(pg.sprite.Sprite):
    def __init__(self, radius, pos):
        super().__init__()
        self.radius = radius
        self.image = pg.Surface((2 * radius, 2 * radius),
                                pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color('pink'),
                       (radius, radius), radius)
        x, y = pos
        self.rect = pg.Rect(x, y, 2 * radius - 5, 2 * radius - 5)
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pg.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy

        if pg.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx

        if pg.sprite.spritecollideany(self, balls):
            self.vx = -self.vx
            self.vy = -self.vy


class Border(pg.sprite.Sprite):
    def __init__(self, x1, x2, y1, y2):
        super().__init__()
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pg.Surface((1, y2 - y1))
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pg.Surface((x2 - x1, 1))
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)


running = True
display = pg.display.set_mode((400, 400))

lb = Border(0, 0, 0, 400)
rb = Border(400, 400, 0, 400)
tb = Border(0, 400, 0, 0)
db = Border(0, 400, 400, 400)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONUP:
            point = event.pos
            balls.add(Ball(20, point))

    fps = pg.time.Clock().tick(30)
    for i, ball in enumerate(balls):
        balls.remove(ball)
        ball.update()
        balls.add(ball)

    display.fill(pg.Color('black'))

    for ball in balls:
        display.blit(ball.image, ball.rect)

    pg.display.flip()

pg.quit()
