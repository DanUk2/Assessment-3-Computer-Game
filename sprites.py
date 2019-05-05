#sprite classes for platform Game
import pygame as pg
from settings import *

vec = pg.math.Vector2


plat = pg.image.load('img/plat.png')

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.walk_frames_r = [pg.image.load('img/runR1.png'), pg.image.load('img/runR2.png'), pg.image.load('img/runR3.png')]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.standing_frames = [pg.image.load('img/idle1.png'), pg.image.load('img/idle2.png'), pg.image.load('img/idle3.png'), pg.image.load('img/idle1.png'), pg.image.load('img/idle1.png')]
        self.jumping_frames = [pg.image.load('img/jump1.png'), pg.image.load('img/jump2.png'), pg.image.load('img/jump3.png')]

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
    def jump(self):
        #jump if on platforms
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP




    def update(self):
        self.animate()
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
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        #
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # walk animation
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 120:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # jump animation
        if self.jumping:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                bottom = self.rect.bottom
                self.image = self.jumping_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = plat
        self.image = pg.transform.scale(plat, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
