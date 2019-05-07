# platformer
import pygame as pg
import random
import pygame, sys
from settings import *
from sprites import *

#HUD functions

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 35
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        #create game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.menu_sound = pg.mixer.Sound('snd/menu.wav')

    def new(self):
        #start new game
        self.shoot_sound = pg.mixer.Sound('snd/shoot.wav')
        self.damage_sound = pg.mixer.Sound('snd/damage.wav')
        self.dink_sound = pg.mixer.Sound('snd/dink.wav')
        # self.menu_sound = pg.mixer.Sound('snd/menu.wav')
        p1wins = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.p1bullets = pg.sprite.Group()
        self.p2bullets = pg.sprite.Group()
        self.crates = pg.sprite.Group()
        self.player2 = Player2(self)
        self.player = Player(self)
        self.winner = p1head
        self.player1wins = p1win0
        self.player2wins = p2win0
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player2)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for crate in CRATE_LIST:
            self.crate = Crate(*crate)
            self.all_sprites.add(self.crate)
            self.crates.add(self.crate)
        pg.mixer.music.load('snd/music.mp3')
        self.run()

    def run(self):
        #game loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        #game loop update
        self.all_sprites.update()
        #check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y <= lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
        # player 2 check
        if self.player2.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player2, self.platforms or self.crates, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player2.pos.y < lowest.rect.centery:
                    self.player2.pos.y = lowest.rect.top
                    self.player2.vel.y = 0
                    self.player2.jumping = False
        #bullets hitting cover
        cover_hit = pg.sprite.groupcollide(self.crates, self.p1bullets, False, True)
        for hit in cover_hit:
            self.dink_sound.play()
            hit.health -= PLAYER_DAMAGE

        cover_hit = pg.sprite.groupcollide(self.crates, self.p2bullets, False, True)
        for hit in cover_hit:
            self.dink_sound.play()
            hit.health -= PLAYER_DAMAGE

        # check if hit
        player_hit = pg.sprite.spritecollide(self.player, self.p2bullets, False)
        if player_hit:
            self.damage_sound.play()
            self.player.health -= PLAYER_DAMAGE
            for self.p2bullet in player_hit:
                self.p2bullet.kill()

        # check if player 2 hit
        player2_hit = pg.sprite.spritecollide(self.player2, self.p1bullets, False)
        if player2_hit:
            self.damage_sound.play()
            self.player2.health -= PLAYER_DAMAGE
            for self.p1bullet in player2_hit:
                self.p1bullet.kill()
        # check if player 1 won
        if self.player2.p1wins == 1:
            self.player1wins = p1win1
        if self.player2.p1wins == 2:
            self.player1wins = p1win2
        if self.player2.p1wins == 3:
            self.winner = p1head
            self.player1wins = p1win3
            self.playing = False
        # check if player 2 won
        if self.player.p2wins == 1:
            self.player2wins = p2win1
        if self.player.p2wins == 2:
            self.player2wins = p2win2
        if self.player.p2wins == 3:
            self.winner = p2head
            self.player2wins = p2win3
            self.playing = False




        #if player reachs end of screen
        # if self.player.rect.left <= WIDTH - 800:
        #     self.player.pos.x += abs(self.player.vel.x)
        #     for plat in self.platforms:
        #         plat.rect.x += abs(self.player.vel.x)
        #
        # if self.player.rect.right >= WIDTH - 224:
        #     self.player.pos.x -= abs(self.player.vel.x)
        #     for plat in self.platforms:
        #         plat.rect.x -= abs(self.player.vel.x)



    def events(self):
        #game loop events
        global left
        global right
        global left2
        global right2

        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # check for jump
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    self.player.jump_cut()
            # detect direction
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                left = True
                right = False

            if keys[pg.K_d]:
                right = True
                left = False
            # check for shoot
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.shoot_sound.play()
                    if right:
                        self.p1bullet = Bullet_right(self.player.rect.centerx, self.player.rect.centery - 5)
                        self.all_sprites.add(self.p1bullet)
                        self.p1bullets.add(self.p1bullet)
                    elif left:
                # if event.key == pg.K_LEFT:
                        self.p1bullet = Bullet_left(self.player.rect.left - 20, self.player.rect.centery - 5)
                        self.all_sprites.add(self.p1bullet)
                        self.p1bullets.add(self.p1bullet)
                    else:
                        self.p1bullet = Bullet_right(self.player.rect.centerx, self.player.rect.centery - 5)
                        self.all_sprites.add(self.p1bullet)
                        self.p1bullets.add(self.p1bullet)
            # player 2 check for jump
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player2.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player2.jump_cut()
            #  player 2 detect direction
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                left2 = True
                right2 = False

            if keys[pg.K_RIGHT]:
                right2 = True
                left2 = False
            # player 2 check for shoot
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RCTRL:
                    self.shoot_sound.play()
                    if right2:
                        self.p2bullet = Bullet_right(self.player2.rect.centerx, self.player2.rect.centery - 5)
                        self.p2bullet.image = bullet2
                        self.all_sprites.add(self.p2bullet)
                        self.p2bullets.add(self.p2bullet)
                    elif left2:
                # if event.key == pg.K_LEFT:
                        self.p2bullet = Bullet_left(self.player2.rect.left - 20, self.player2.rect.centery - 5)
                        self.p2bullet.image = bullet2left
                        self.all_sprites.add(self.p2bullet)
                        self.p2bullets.add(self.p2bullet)
                    else:
                        self.p2bullet = Bullet_right(self.player2.rect.centerx, self.player2.rect.centery - 5)
                        self.p2bullet.image = bullet2
                        self.all_sprites.add(self.p2bullet)
                        self.p2bullets.add(self.p2bullet)
                # if event.key == pg.K_UP:
                #     self.bullet = Bullet_up(self.player.rect.centerx - 25, self.player.rect.top - 30)
                #     self.all_sprites.add(self.bullet)
                #     self.bullets.add(self.bullet)

    def draw(self):
        #game loop draw
        self.screen.blit(bg, (0, 0))
        self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            if isinstance(sprite, Crate):
                sprite.draw_health()
        self.screen.blit(self.player2.image, self.player2.rect)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(p1head, (20, 5))
        self.screen.blit(p2head, (WIDTH - 103, 5))
        self.screen.blit(self.player1wins, (100, 80))
        self.screen.blit(self.player2wins, (WIDTH - 180, 80))
        draw_player_health(self.screen, 100, 35, self.player.health / PLAYER_HEALTH)
        draw_player_health(self.screen, WIDTH - 300, 35, self.player2.health / PLAYER_HEALTH)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        #start screen
        self.screen.blit(ts, (0, 0))
        pg.display.flip()
        self.wait_for_key()


    def show_go_screen(self):
        #game over screen
        if not self.running:
            return
        self.screen.blit(ws, (0, 0))
        self.screen.blit(self.winner, (WIDTH / 2, HEIGHT / 2))
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
                if event.type == pg.KEYUP:
                    self.menu_sound.play()
                    waiting = False

    def draw_text(self, text, size, colour, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
