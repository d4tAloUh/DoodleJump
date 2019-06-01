import random

from Src.Sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc
        self.multiplayer = False
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
        if not self.multiplayer:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        else:
            self.screen = pg.display.set_mode((WIDTH * 2 + 20, HEIGHT))
        self.score = [0,0]
        self.players = [Player(self, WIDTH / 2, HEIGHT - 40, WIDTH, 0),
                        Player(self, WIDTH * 3/2, HEIGHT - 40, WIDTH*2 + 20, WIDTH + 20, True)]
        self.difficulty_counter = [1,1]
        self.monster_possibility = MONSTER_POSSIBILITY
        self.timer = 0
        self.bullet_timer = 0
        self.bullet_timer_2 = 0

        self.start_buttons = pg.sprite.Group()
        self.all_sprites_1 = pg.sprite.Group()
        self.all_sprites_2 = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bullets_2 = pg.sprite.Group()
        self.platforms_1 = pg.sprite.Group()
        self.platforms_2 = pg.sprite.Group()

        self.background_sprite = pg.sprite.Group()
        self.gameover_sprite = pg.sprite.Group()
        self.springs = pg.sprite.Group()
        self.springs_2 = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.monsters_2 = pg.sprite.Group()

        self.background = Background(BACKGROUND)
        self.background_2 = Background(BACKGROUND, True)
        self.background_skies = Background(BACKGROUND_SKIES)
        self.background_skies_2 = Background(BACKGROUND_SKIES, True)

        self.platfor_amount = PLATFORM_AMOUNT

        self.gameover = Background(GAMEOVER)
        self.all_sprites_1.add(self.players[0])
        if self.multiplayer:
            self.all_sprites_2.add(self.players[1])
            self.background_sprite.add(self.background_skies_2)
            self.background_sprite.add(self.background_2)
        self.background_sprite.add(self.background_skies)
        self.background_sprite.add(self.background)
        self.gameover_sprite.add(self.gameover)
        # self.start_sprite.add(self.start)

        # Draw platforms for 1st player
        for plat in PLATFORM_LIST_1:
            p = Platform(self, *plat, 0, WIDTH, False)
            self.all_sprites_1.add(p)
            self.platforms_1.add(p)
        # Draw platforms for 2st player
        if self.multiplayer:
            for plat in PLATFORM_LIST_2:
                p = Platform(self, *plat,WIDTH +20, 2*WIDTH + 20, False)
                self.all_sprites_2.add(p)
                self.platforms_2.add(p)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        self.playing_2 = False
        if self.multiplayer:
            self.playing_2 = True
        while self.playing or self.playing_2:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites_1.update()
        self.all_sprites_2.update()
        self.now = pg.time.get_ticks()

        # check if player hits platform
        if self.playing:
            if self.players[0].vel.y > 0:
                hits1 = pg.sprite.spritecollide(self.players[0], self.platforms_1, False)
                if hits1:
                    lowest = hits1[0]
                    for hit in hits1:
                        if hit.rect.bottom > lowest.rect.bottom:
                            lowest = hit
                    if self.players[0].pos.y > lowest.rect.centery:
                        if lowest.type == 'brown':
                            # lowest.animate(self.now)
                            lowest.set_brown(True)
                        else:
                            self.players[0].pos.y = lowest.rect.top
                            self.players[0].vel.y = 0
                            self.players[0].jump()
        # Check if second player hits platform
        if self.multiplayer and self.playing_2:
            hits2 = pg.sprite.spritecollide(self.players[1], self.platforms_2, False)
            if hits2:
                lowest2 = hits2[0]
                for hit in hits2:
                    if hit.rect.bottom > lowest2.rect.bottom:
                        lowest2 = hit
                if self.players[1].pos.y > lowest2.rect.centery:
                    if lowest2.type == 'brown':
                        # lowest.animate(self.now)
                        lowest2.set_brown(True)
                    else:
                        self.players[1].pos.y = lowest2.rect.top
                        self.players[1].vel.y = 0
                        self.players[1].jump()
        # If player1 reaches top 1/4
        if self.playing:
            if self.players[0].rect.top <= HEIGHT / 3.5:
                self.players[0].pos.y += max(abs(self.players[0].vel.y), 4)
                for monster in self.monsters:
                    monster.rect.y += max(abs(self.players[0].vel.y), 5)
                for plat in self.platforms_1:
                    plat.rect.y += max(abs(self.players[0].vel.y), 4)
                    if plat.rect.top >= HEIGHT:
                        plat.kill()
                        self.score[0] += 10
        # if player2 reaches top 1/4
        if self.multiplayer and self.playing_2:
            if self.players[1].rect.top <= HEIGHT / 4:
                self.players[1].pos.y += max(abs(self.players[1].vel.y), 4)
                for monster1 in self.monsters_2:
                    monster1.rect.y += max(abs(self.players[1].vel.y), 5)
                for plat2 in self.platforms_2:
                    plat2.rect.y += max(abs(self.players[1].vel.y), 4)
                    if plat2.rect.top >= HEIGHT:
                        plat2.kill()
                        self.score[1] += 10
        # Spawn monster
        if self.now - self.timer > self.monster_possibility + random.choice([-1000, 1000, 500, 0, -500]):
            self.timer = self.now
            if self.playing:
                Enemy(self, WIDTH, 0)
            if self.multiplayer and self.playing_2:
                Enemy(self, WIDTH*2 + 20, WIDTH + 20, True)

        # Hit monster
        if self.playing:
            mob_hits = pg.sprite.spritecollide(self.players[0], self.monsters, False, pg.sprite.collide_mask)
            if mob_hits:
                self.playing = False

        if self.multiplayer and self.playing_2:
            mob_hits1 = pg.sprite.spritecollide(self.players[1], self.monsters_2, False, pg.sprite.collide_mask)
            if mob_hits1:
                self.playing_2 = False

        # Create new platforms
        if self.playing:
            while len(self.platforms_1) < self.platfor_amount:
                width = random.randrange(75, 100)
                p = Platform(self, random.randrange(0, WIDTH - width), random.randrange(-150, -30), 0, WIDTH, False)
                self.platforms_1.add(p)
                self.all_sprites_1.add(p)

        if self.multiplayer and self.playing_2:
            while len(self.platforms_2) < PLATFORM_AMOUNT:
                width = random.randrange(75, 100)
                s = Platform(self, random.randrange(WIDTH, 2 * WIDTH - width),
                             random.randrange(-150, -30), WIDTH+ 20, 2*WIDTH + 20, False)
                self.platforms_2.add(s)
                self.all_sprites_2.add(s)

        #   Death
        if self.playing:
            if self.players[0].rect.bottom > HEIGHT:
                for sprit in self.all_sprites_1:
                    sprit.rect.y -= max(self.players[0].vel.y, 5)
                    if sprit.rect.bottom < 0:
                        sprit.kill()
                    if len(self.platforms_1) == 0:
                        self.playing = False

        if self.multiplayer and self.playing_2:
            if self.players[1].rect.bottom > HEIGHT:
                for sprite in self.all_sprites_2:
                    sprite.rect.y -= max(self.players[1].vel.y, 5)
                    if sprite.rect.bottom < 0:
                        sprite.kill()
                    if len(self.platforms_2)  == 0:
                        self.playing_2 = False


        # Increase level difficulty
        if self.score[0] > 1000 and (self.score[0] / 200) / 2 > self.difficulty_counter[0]:
            self.difficulty_counter[0] += 2
            if not self.platfor_amount == 8:
                self.platfor_amount -= 1
            if self.monster_possibility > 5000:
                self.monster_possibility -= 100
        if 2060 > self.score[0] > 2000:
            # self.all_sprites.add(self.background_skies)
            self.background_sprite.remove(self.background)

        #     Collide with spring
        if self.playing:
            spring_hits = pg.sprite.spritecollide(self.players[0], self.springs, False)
            for spring in spring_hits:
                if spring.type == 'spring':
                    spring.animate()
                    self.players[0].vel.y = - BOOST
        if self.multiplayer and self.playing_2:
            spring_hits2 = pg.sprite.spritecollide(self.players[1], self.springs_2, False)
            for spring1 in spring_hits2:
                if spring1.type == 'spring':
                    spring1.animate()
                    self.players[1].vel.y = - BOOST

        #     Monster collide with bullet
        if self.playing:
            bullet_hits = pg.sprite.groupcollide(self.bullets, self.monsters, True, True)
            for hit in bullet_hits:
                hit.kill()
                self.score[0] += 50
        if self.playing_2 and self.multiplayer:
            bullet_hits1 = pg.sprite.groupcollide(self.bullets_2, self.monsters, True, True)
            for hit in bullet_hits1:
                hit.kill()
                self.score[1] += 50

    def events(self):

        # Game Loop - eventsF
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing or self.playing_2:
                    self.playing = False
                    self.playing_2 = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if self.playing:
                    if event.key == pg.K_UP:
                        if self.now - self.bullet_timer > 500:
                            self.bullet_timer = self.now
                            Bullet(self, self.players[0])
                if self.playing_2 and self.multiplayer:
                    if event.key == pg.K_w:
                        if self.now - self.bullet_timer_2 > 500:
                            self.bullet_timer_2 = self.now
                            Bullet(self, self.players[1])

    def draw(self):
        # Game Loop - draw
        # self.screen.fill(BGCOLOR)
        self.background_sprite.draw(self.screen)
        pg.draw.rect(self.screen,BLACK,[WIDTH,0,20,HEIGHT])
        self.all_sprites_1.draw(self.screen)
        self.all_sprites_2.draw(self.screen)
        self.screen.blit(self.players[0].image, self.players[0].rect)
        # Draw score
        self.draw_text(str(self.score[0]), 22, BLACK, WIDTH / 2, 20)
        self.draw_text(str(self.score[1]), 22, BLACK, WIDTH * 3/ 2, 20)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.start_button = Button(self.screen, 72, 150, "esjketit", (255, 255, 255), 150, 70)
        self.multiplayer_button = Button(self.screen, 133, 230, "esjketit", (255, 255, 255), 150, 70)
        self.start_sprite.draw(self.screen)
        # self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use left and right keys to move", 36, BLACK, WIDTH / 2, HEIGHT * 2.5 / 4 + 30)
        self.draw_text("and up key to shoot", 36, BLACK, WIDTH / 2 + 20, HEIGHT * 2 / 3 + 50)
        # self.draw_text("Press SPACE to start", 36, BLACK, WIDTH / 2, HEIGHT / 2.5)
        self.draw_text("Highscore: " + str(self.highscore), 22, BROWN, WIDTH * 3 / 4 + 10, HEIGHT / 4 + 20)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.gameover_sprite.draw(self.screen)

        # self.draw_text("GAME OVER", 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("" + str(self.score[0]), 42, BROWN, WIDTH * 4 / 5 + 25, HEIGHT / 2 - 15)
        self.draw_text("Press space to play again", 36, BLACK, WIDTH / 2 , HEIGHT * 2 / 3)
        if self.score[0] > self.highscore:
            self.highscore = self.score[0]
            self.draw_text("You have a new highscore!", 36, BLACK, WIDTH / 2 + 30, HEIGHT / 2 -40)
            file = open(HIGHSCORE, 'w')
            file.write(str(self.highscore))
            file.close()
        else:
            self.draw_text("Highscore: " + str(self.highscore), 22, RED, WIDTH * 4 / 5 + 18, HEIGHT / 3 - 35)
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
                    if self.multiplayer_button.rect.collidepoint(pg.mouse.get_pos()):
                        self.multiplayer = True
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
