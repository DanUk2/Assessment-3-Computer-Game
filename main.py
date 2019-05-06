# platformer
import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        #create game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        #start new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player2 = Player2(self)
        self.player = Player(self)
        self.health_bars = health_bars()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player2)
        self.p1bullets = pg.sprite.Group()
        self.p2bullets = pg.sprite.Group()
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

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
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
        # player 2 check
        if self.player2.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player2, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player2.pos.y < lowest.rect.centery:
                    self.player2.pos.y = lowest.rect.top
                    self.player2.vel.y = 0
                    self.player2.jumping = False

        # check if hit
        player_hit = pg.sprite.spritecollide(self.player, self.p2bullets, False)
        if player_hit:
            self.player.health -= 1
            for self.p2bullet in player_hit:
                self.p2bullet.kill()

        # check if player 2 hit
        player2_hit = pg.sprite.spritecollide(self.player2, self.p1bullets, False)
        if player2_hit:
            self.player2.health -= 1
            for self.p1bullet in player2_hit:
                self.p1bullet.kill()

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
        self.screen.blit(self.player2.image, self.player2.rect)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.health_bars.health_bar1, self.health_bars.bar1_rect)
        self.screen.blit(self.health_bars.health_bar2, self.health_bars.bar2_rect)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        #start screen
        pass

    def show_go_screen(self):
        #game over screen
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
