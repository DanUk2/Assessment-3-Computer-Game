#sprite classes for platform Game
import pygame as pg
from settings import *

vec = pg.math.Vector2


walkRight = [pg.image.load('img/runR1.png'), pg.image.load('img/runR2.png'), pg.image.load('img/runR3.png')]
walkLeft = [pg.image.load('img/runL1.png'), pg.image.load('img/runL2.png'), pg.image.load('img/runL3.png')]
char = pg.image.load('img/idle.png')
plat = pg.image.load('img/plat.png')

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.image = char


        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)


    def jump(self):
        #jump if on platforms
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            self.vel.y = -20




    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC


        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC




        #apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = plat
        self.image = pg.transform.scale(plat, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
