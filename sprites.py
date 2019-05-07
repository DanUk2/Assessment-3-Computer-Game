#sprite classes for platform Game
import pygame as pg
from settings import *
import random

vec = pg.math.Vector2


plat = pg.image.load('img/plat.png')
bullet = pg.image.load('img/bullet.png')
bullet2 = pg.image.load('img/bullet2.png')
bullet2left = pg.transform.flip(bullet2, True, False)
bg = pg.image.load('img/bg.png')
ts = pg.image.load('img/titlescreen.png')
ws = pg.image.load('img/winscreen.png')
p1head = pg.image.load('img/p1head.png')
p2head = pg.image.load('img/p2head.png')
crate = pg.image.load('img/crate.png')
p1win0 = pg.image.load('img/p1/win0.png')
p1win1 = pg.image.load('img/p1/win1.png')
p1win2 = pg.image.load('img/p1/win2.png')
p1win3 = pg.image.load('img/p1/win3.png')
p2win0 = pg.image.load('img/p2/win0.png')
p2win1 = pg.image.load('img/p2/win1.png')
p2win2 = pg.image.load('img/p2/win2.png')
p2win3 = pg.image.load('img/p2/win3.png')





left = False
right = False


spawnpoints = [(40, 400), (WIDTH - 40, 400), (40, 200), (WIDTH - 40, 200), (WIDTH / 2, 100), (WIDTH / 2, 180)]

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.p2wins = 0
        self.health = PLAYER_HEALTH
        self.walking = False
        self.jumping = False
        self.shooting = False
        self.left = False
        self.right = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.load_sounds()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, 400)
        self.pos = vec(40, 400)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_sounds(self):
        self.jump_sound = pg.mixer.Sound('snd/jump.wav')
    def load_images(self):
        self.standing_frames_r = [pg.image.load('img/p1/shooting3.png')]
        self.standing_frames_l = []
        for frame in self.standing_frames_r:
            self.standing_frames_l.append(pg.transform.flip(frame, True, False))
        self.jumping_frames_r = [pg.image.load('img/p1/jump1.png'), pg.image.load('img/p1/jump2.png'), pg.image.load('img/p1/jump3.png'), pg.image.load('img/p1/jump3.png'), pg.image.load('img/p1/jump3.png'), pg.image.load('img/p1/jump3.png'), pg.image.load('img/p1/jump3.png')]
        self.jumping_frames_l = []
        for frame in self.jumping_frames_r:
            self.jumping_frames_l.append(pg.transform.flip(frame, True, False))
        self.shooting_frames_r = [pg.image.load('img/p1/runShoot1.png'), pg.image.load('img/p1/runShoot2.png'), pg.image.load('img/p1/runShoot3.png')]
        self.shooting_frames_l = []
        for frame in self.shooting_frames_r:
            self.shooting_frames_l.append(pg.transform.flip(frame, True, False))

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
            self.jump_sound.play()
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

        # player death
        if self.health <= 0:
            self.respawn()

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
                self.current_frame = (self.current_frame + 1) % len(self.shooting_frames_l)
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

    def respawn(self):
        self.p2wins += 1
        self.health = PLAYER_HEALTH
        self.pos = vec(random.choice(spawnpoints))
        self.rect.center = self.pos

class Player2(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.p1wins = 0
        self.health = PLAYER_HEALTH
        self.walking = False
        self.jumping = False
        self.shooting = False
        self.left = False
        self.right = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.load_sounds()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 40, 400)
        self.pos = vec(WIDTH - 40, 400)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_sounds(self):
        self.jump_sound = pg.mixer.Sound('snd/jump.wav')
    def load_images(self):
        self.standing_frames_r = [pg.image.load('img/p2/shooting3.png')]
        self.standing_frames_l = []
        for frame in self.standing_frames_r:
            self.standing_frames_l.append(pg.transform.flip(frame, True, False))
        self.jumping_frames_r = [pg.image.load('img/p2/jump1.png'), pg.image.load('img/p2/jump2.png'), pg.image.load('img/p2/jump3.png'), pg.image.load('img/p2/jump3.png'), pg.image.load('img/p2/jump3.png'), pg.image.load('img/p2/jump3.png'), pg.image.load('img/p2/jump3.png')]
        self.jumping_frames_l = []
        for frame in self.jumping_frames_r:
            self.jumping_frames_l.append(pg.transform.flip(frame, True, False))
        self.shooting_frames_r = [pg.image.load('img/p2/runShoot1.png'), pg.image.load('img/p2/runShoot2.png'), pg.image.load('img/p2/runShoot3.png')]
        self.shooting_frames_l = []
        for frame in self.shooting_frames_r:
            self.shooting_frames_l.append(pg.transform.flip(frame, True, False))

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
            self.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.left = True
            self.right = False

        if keys[pg.K_RIGHT]:
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

        # player death
        if self.health <= 0:
            self.respawn()

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
                self.current_frame = (self.current_frame + 1) % len(self.shooting_frames_l)
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

    def respawn(self):
        self.p1wins += 1
        self.health = PLAYER_HEALTH
        self.pos = vec(random.choice(spawnpoints))
        self.rect.center = self.pos

class Crate(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = crate
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 400
    def update(self):
        if self.health <= 0:
            self.kill()
    def draw_health(self):
        if self.health > 200 * 0.6:
            col = GREEN
        elif self.health > 200 * 0.3:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / 100)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < 200:
            pg.draw.rect(self.image, col, self.health_bar)

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



    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
