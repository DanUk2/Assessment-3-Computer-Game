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
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.bullets = pg.sprite.Group()
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
        #if player reachs end of screen
        if self.player.rect.left <= WIDTH - 800:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)

        if self.player.rect.right >= WIDTH - 224:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)



    def events(self):
        #game loop events
        global left
        global right
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
                        self.bullet = Bullet_right(self.player.rect.centerx, self.player.rect.top)
                        self.all_sprites.add(self.bullet)
                        self.bullets.add(self.bullet)
                    elif left:
                # if event.key == pg.K_LEFT:
                        self.bullet = Bullet_left(self.player.rect.left - 20, self.player.rect.top)
                        self.all_sprites.add(self.bullet)
                        self.bullets.add(self.bullet)
                    else:
                        self.bullet = Bullet_right(self.player.rect.centerx, self.player.rect.top)
                        self.all_sprites.add(self.bullet)
                        self.bullets.add(self.bullet)
                # if event.key == pg.K_UP:
                #     self.bullet = Bullet_up(self.player.rect.centerx - 25, self.player.rect.top - 30)
                #     self.all_sprites.add(self.bullet)
                #     self.bullets.add(self.bullet)




    def draw(self):
        #game loop draw
        self.screen.blit(bg, (0,0))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
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
