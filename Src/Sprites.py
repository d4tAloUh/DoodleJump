from random import choice, randrange

import pygame as pg
from Src.Settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, x1, x2, second=False):
        self._layer = 1
        # Width
        self.x1 = x1
        # 0
        self.x2 = x2
        pg.sprite.Sprite.__init__(self)
        self.game = game  #
        self.last_tick = 0
        self.second = second
        self.side_frames = [pg.image.load(DOODLE_RIGHT), pg.image.load(DOODLE_LEFT), pg.image.load(DOODLE_UP)]
        self.image = self.side_frames[0]
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0.7)
        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        bottom = self.rect.bottom
        if not self.second:
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
        else:
            if keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC
                self.image = self.side_frames[1]
            if keys[pg.K_d]:
                self.acc.x = PLAYER_ACC
                self.image = self.side_frames[0]
            if keys[pg.K_w]:
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
        if self.pos.x > self.x1:
            self.pos.x = self.x2
        if self.pos.x < self.x2:
            self.pos.x = self.x1

        self.rect.midbottom = self.pos
        self.mask = pg.mask.from_surface(self.image)

    def jump(self):
        #       Jump only when standing on anything
        self.rect.y += 1
        if not self.second:
            hits = pg.sprite.spritecollide(self, self.game.platforms_1, False)
        else:
            hits2 = pg.sprite.spritecollide(self, self.game.platforms_2, False)
        self.rect.y -= 1
        if self.second and hits2:
            self.vel.y -= PlAYER_JUMP
        elif not self.second and hits:
            self.vel.y -= PlAYER_JUMP


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, end, brown=False):
        self.collision = brown
        self.width = width
        self.end = end
        self._layer = 2
        self.moment = 0
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.images = [pg.image.load(PLATFORM_GREEN).convert(), pg.image.load(PLATFORM_BLUE)]
        self.brown = [pg.image.load(PLATFORM_BROWN_1), pg.image.load(PLATFORM_BROWN_2),
                      pg.image.load(PLATFORM_BROWN_3), pg.image.load(PLATFORM_BROWN_4),
                      pg.image.load(PLATFORM_BROWN_5), pg.image.load(PLATFORM_BROWN_6)]
        self.images[0].set_colorkey(BLACK)
        self.number = randrange(0, 100)
        if self.number < 50 or self.game.score[0] < 60:
            self.type = 'green'
            self.image = self.images[0]
        elif 50 < self.number < 85:
            self.type = 'blue'
            self.image = self.images[1]
        else:
            self.type = 'brown'
            self.image = self.brown[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_frame = 0
        self.vx = randrange(1, 4)
        self.number = randrange(0, 100, 2)

        if self.type == 'green' and randrange(100) < SPRING_POSSIBILITY:
            Spring(self.game, self)

    def set_brown(self, brown):
        self.collision = brown

    def update(self, *args):

        if self.type == 'blue':
            self.rect.x += self.vx
            if self.rect.x > self.end - 50 or self.rect.x < self.width:
                self.vx *= -1
        if self.type == 'brown':
            if self.collision:
                self.animate()

    def animate(self):

        now = pg.time.get_ticks()
        if now - self.moment > 40:
            self.moment = now
            self.current_frame = (self.current_frame + 1)
            center = self.rect.center
            self.image = self.brown[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
            if self.current_frame == 5:
                self.kill()


class Background(pg.sprite.Sprite):
    def __init__(self, image, secondPlayer=False):
        self._layer = 3
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image).convert()
        self.rect = self.image.get_rect()
        if not secondPlayer:
            self.rect.x, self.rect.y = 0, 0
        else:
            self.rect.x, self.rect.y = WIDTH + 20, 0


class Spring(pg.sprite.Sprite):
    def __init__(self, game, platform):
        self._layer = 2
        self.game = game
        if not self.game.multiplayer:
            self.groups = game.all_sprites, game.springs
        else:
            self.groups = game.all_sprites, game.springs_2
        pg.sprite.Sprite.__init__(self, self.groups)
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
        if self.game.multiplayer:
            if not self.game.platforms_2.has(self.plat):
                self.kill()
        if not self.game.platforms_1.has(self.plat):
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
    def __init__(self, game, x1, x2, second=False):
        self._layer = 1
        # Width
        self.x1 = x1
        # Zero
        self.x2 = x2
        self.second = second
        if self.second:
            self.groups = game.monsters, game.all_sprites
        else:
            self.groups = game.monsters_2, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.images = [pg.transform.scale(pg.image.load(MONSTER_UP), (83, 47)),
                       pg.transform.scale(pg.image.load(MONSTER_DOWN), (83, 47))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([self.x2, self.x1 - 10])
        self.vx = randrange(3, 6)
        if self.rect.centerx > self.x1 - 30:
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
        if self.rect.left > self.x1 + 10 or self.rect.right < self.x2:
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


class Button:

    def __init__(self, screen, x, y, text, color, width=70, height=40):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.rect = pg.Rect(x, y, width, height)
        self.show()

    def show(self):
        self.draw_button()
        self.write_text()

    def write_text(self):
        font = pg.font.Font(pg.font.match_font(FONT_NAME), 24)
        label = font.render(self.text, 1, self.color)
        self.screen.blit(label, ((self.x + self.width / 2) - label.get_width() / 2,
                                 (self.y + self.height / 2) - label.get_height() / 2))

    def draw_button(self):
        pg.draw.rect(self.screen, self.color, self.rect, 0)
        pg.draw.rect(self.screen, self.color, self.rect, 1)
