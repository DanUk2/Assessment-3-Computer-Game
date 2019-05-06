#sprite classes for platform Game
import pygame as pg
from settings import *

vec = pg.math.Vector2


plat = pg.image.load('img/plat.png')
bullet = pg.image.load('img/bullet.png')
bg = pg.image.load('img/bg.png')


left = False
right = False




class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.shooting = False
        self.left = False
        self.right = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames_r[0]
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
        self.standing_frames_r = [pg.image.load('img/shooting3.png')]
        self.standing_frames_l = []
        for frame in self.standing_frames_r:
            self.standing_frames_l.append(pg.transform.flip(frame, True, False))
        self.jumping_frames_r = [pg.image.load('img/jump1.png'), pg.image.load('img/jump2.png'), pg.image.load('img/jump3.png'), pg.image.load('img/jump3.png'), pg.image.load('img/jump3.png'), pg.image.load('img/jump3.png'), pg.image.load('img/jump3.png')]
        self.jumping_frames_l = []
        for frame in self.jumping_frames_r:
            self.jumping_frames_l.append(pg.transform.flip(frame, True, False))
        self.shooting_frames_r = [pg.image.load('img/runShoot1.png'), pg.image.load('img/runShoot2.png'), pg.image.load('img/runShoot3.png')]
        self.shooting_frames_l = []
        for frame in self.shooting_frames_r:
            self.shooting_frames_l.append(pg.transform.flip(frame, True, False))
        self.shootingIdle_frames_r = [pg.image.load('img/shooting1.png'), pg.image.load('img/shooting2.png'), pg.image.load('img/shooting3.png')]
        self.shootingIdle_frames_l = []
        for frame in self.shootingIdle_frames_r:
            self.shootingIdle_frames_l.append(pg.transform.flip(frame, True, False))

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
            self.left = True
            self.right = False

        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
            self.right = True
            self.left = False

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
        if self.vel.x != 0 and not self.jumping:
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
                    self.image = self.shooting_frames_r[self.current_frame]
                else:
                    self.image = self.shooting_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # idle animation
        if not self.jumping and not self.walking and not self.shooting:
            if now - self.last_update > 120:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames_r)
                bottom = self.rect.bottom
                if self.right:
                    self.image = self.standing_frames_r[self.current_frame]
                if self.left:
                    self.image = self.standing_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # jump animation
        if self.jumping:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames_l)
                bottom = self.rect.bottom
                if self.right:
                    self.image = self.jumping_frames_r[self.current_frame]
                if self.left:
                    self.image = self.jumping_frames_l[self.current_frame]
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

class Bullet_right(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PROJECTILE_SPEED
        self.player = Player(self)
        self.player.shooting = True

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

class Bullet_left(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet
        self.image = pg.transform.flip(bullet, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PROJECTILE_SPEED
        self.player = Player(self)
        self.player.shooting = True


    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# class Bullet_up(pg.sprite.Sprite):
#     def __init__(self, x, y):
#         pg.sprite.Sprite.__init__(self)
#         self.image = bullet
#         self.image = pg.transform.rotate(bullet, 90)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.speed = PROJECTILE_SPEED
#
#
#     def update(self):
#         self.rect.y -= self.speed
#         if self.rect.bottom < 0:
#             self.kill()
