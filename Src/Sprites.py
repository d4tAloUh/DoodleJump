from random import choice, randrange

import pygame as pg
from Src.Settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = 1
        pg.sprite.Sprite.__init__(self)
        self.game = game  #
        self.last_tick = 0
        self.side_frames = [pg.image.load(DOODLE_RIGHT), pg.image.load(DOODLE_LEFT), pg.image.load(DOODLE_UP)]
        self.image = self.side_frames[0]
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 40)
        self.pos = vec(WIDTH / 2, HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0.7)
        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        bottom = self.rect.bottom
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.image = self.side_frames[1]
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.image = self.side_frames[0]
        if keys[pg.K_UP]:
            self.image = self.side_frames[2]
            if now - self.last_tick > 300:
                self.last_tick = now
                self.image = self.side_frames[1]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + PLAYER_GRAVITY * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
        self.mask = pg.mask.from_surface(self.image)

    def jump(self):
        #       Jump only when standing on anything
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y -= PlAYER_JUMP


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 2
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [pg.image.load(PLATFORM_GREEN).convert(), pg.image.load(PLATFORM_BLUE)]
        images[0].set_colorkey(BLACK)
        self.image = choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < SPRING_POSSIBILITY:
            Spring(self.game, self)


class Background(pg.sprite.Sprite):
    def __init__(self, image):
        self._layer = 3
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


class Spring(pg.sprite.Sprite):
    def __init__(self, game, platform):
        self._layer = 2
        self.groups = game.all_sprites, game.springs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.last_update = 0
        self.plat = platform
        self.type = choice(['spring'])
        self.images = [pg.image.load(SPRING_ON), pg.image.load(SPRING_OFF)]
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.rect.centerx = platform.rect.centerx
        self.rect.bottom = platform.rect.top + 2

    def update(self):
        self.rect.bottom = self.plat.rect.top + 2
        if not self.game.platforms.has(self.plat):
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()
        bottom = self.rect.bottom
        self.image = self.images[0]
        if now - self.last_update < 400:
            self.last_update = now
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.image = self.images[1]


class Enemy(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = 1
        self.groups = game.monsters, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.images = [pg.transform.scale(pg.image.load(MONSTER_UP), (83, 47)),
                       pg.transform.scale(pg.image.load(MONSTER_DOWN), (83, 47))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(3, 6)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self, *args):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.mask = pg.mask.from_surface(self.image)
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, player):
        self._layer = 1
        self.groups = game.bullets, game.all_sprites

        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(BULLET)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.centerx
        self.rect.bottom = player.rect.top
        self.vy = -8
        # self.dy =

    def update(self, *args):
        # if self.vy > -8:
        #     self.vy -= self.dy
        # self.mask = pg.mask.from_surface(self.image)
        self.rect.y += self.vy
        if self.rect.bottom < 0:
            self.kill()
