import pygame as pg
import random
from Src.Settings import *
from Src.Sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        # start menu
        self.start_sprite = pg.sprite.Group()
        self.start = Background(START)
        self.start_sprite.add(self.start)
        self.load_data()

    def new(self):
        # start a new game
        self.score = 0
        self.timer = 0
        self.bullet_timer = 0
        self.platform_timer = 0

        self.start_buttons = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.background_sprite = pg.sprite.Group()
        self.gameover_sprite = pg.sprite.Group()
        self.springs = pg.sprite.Group()
        self.monsters = pg.sprite.Group()

        self.player = Player(self)
        self.background = Background(BACKGROUND)

        self.gameover = Background(GAMEOVER)
        self.all_sprites.add(self.player)
        self.background_sprite.add(self.background)
        self.gameover_sprite.add(self.gameover)
        self.start_sprite.add(self.start)
        self.all_sprites.add(self.background)

        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.now = pg.time.get_ticks()
        # check if player hits platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y > lowest.rect.centery:
                    if lowest.type == 'brown':
                        # lowest.animate(self.now)
                        lowest.kill()
                        i = 1
                    else:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jump()
        # If player reaches top 1/4
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 4)
            for monster in self.monsters:
                monster.rect.y += max(abs(self.player.vel.y), 4)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 4)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
        # Spawn monster
        if self.now - self.timer > 5000 + random.choice([-1000, 1000, 500, 0, -500]):
            self.timer = self.now
            Enemy(self)
        # Hit monster
        mob_hits = pg.sprite.spritecollide(self.player, self.monsters, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        # Create new platforms
        while len(self.platforms) < PLATFORM_AMOUNT:
            width = random.randrange(75, 100)
            p = Platform(self, random.randrange(0, WIDTH - width), random.randrange(-150, -30))
            self.platforms.add(p)
            self.all_sprites.add(p)

        #   Death
        if self.player.rect.bottom > HEIGHT:
            for sprit in self.all_sprites:
                sprit.rect.y -= (self.player.vel.y)
                if sprit.rect.bottom < 0:
                    sprit.kill()
            if len(self.platforms) == 0:
                self.playing = False

        #     Collide with spring
        spring_hits = pg.sprite.spritecollide(self.player, self.springs, False)
        for spring in spring_hits:
            if spring.type == 'spring':
                spring.animate()
                self.player.vel.y = - BOOST

        #     Monster collide with bullet
        bullet_hits = pg.sprite.groupcollide(self.bullets, self.monsters, True, True)
        for hit in bullet_hits:
            hit.kill()
            self.score += 50

    def events(self):

        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if self.now - self.bullet_timer > 500:
                        self.bullet_timer = self.now
                        Bullet(self, self.player)

    def draw(self):
        # Game Loop - draw
        # self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        # Draw score
        self.draw_text(str(self.score), 22, BLACK, WIDTH / 2, 20)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.start_button = Button(self.screen, 72, 150, "esjketit", (255, 255, 255), 150, 70)
        self.start_sprite.draw(self.screen)
        # self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use left and right keys to move", 36, BLACK, WIDTH / 2, HEIGHT * 2.5 / 4 + 30)
        self.draw_text("and up key to shoot", 36, BLACK, WIDTH / 2 + 20, HEIGHT *2/3 + 50)
        self.draw_text("Press SPACE to start", 36, BLACK, WIDTH / 2, HEIGHT /2.5)
        self.draw_text("Highscore: " + str(self.highscore), 22,RED, WIDTH *3/4+ 10, HEIGHT /4 + 20)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.gameover_sprite.draw(self.screen)

        # self.draw_text("GAME OVER", 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("" + str(self.score), 42, BROWN, WIDTH / 2 + 27, HEIGHT * 2 / 3 - 24)
        self.draw_text("Press a key to play again", 36, BLACK, WIDTH / 2 + 60, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("You have a new highscore!", 36, BLACK, WIDTH / 2 + 50, HEIGHT / 2 + 20)
            file = open(HIGHSCORE, 'w')
            file.write(str(self.highscore))
            file.close()
        else:
            self.draw_text("Highscore: " + str(self.highscore), 22, BLACK, WIDTH / 2 - 5, HEIGHT / 2 + 20)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.start_button.rect.collidepoint(pg.mouse.get_pos()):
                        waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def draw_text(self, text, font_size, color, x, y):
        font = pg.font.Font(self.font_name, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        #         load all data
        file = open(HIGHSCORE, 'r')
        score_str = file.read()
        file.close()

        try:
            self.highscore = int(score_str)
        except:
            self.highscore = 0





g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
