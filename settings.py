#game options
TITLE = "MEGABATTLE"
WIDTH = 960
HEIGHT = 540
FPS = 60
FONT_NAME = 'arial'

#player properties

PLAYER_HEALTH = 200
PLAYER_ACC = 1
PLAYER_FRICTION = -0.15
PLAYER_GRAV = 0.8
PLAYER_JUMP = 17
PLAYER_DAMAGE = 25


PROJECTILE_SPEED = 10

#starting platforms (x, y, w, h)
PLATFORM_LIST = [(0, 500, 341, 50), (341, 500, 341, 50), (682, 500, 341, 50),
                (0, HEIGHT / 2, 200, 25),
                (WIDTH - 200, HEIGHT / 2, 200, 25),
                (WIDTH / 2 - 175, 380, 350, 25),
                (WIDTH / 2 - 300, 150, 600, 25)]
#crate spawn (x,y)
CRATE_LIST = [(150, 440), (WIDTH - 170, 440), (500, 320)]

# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
