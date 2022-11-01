# content from kids can code: http://kidscancode.org/blog/

# sources
# getting mouse position: https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.get_pos
# shorthand for loops (used in getting mouse collision with sprite): https://stackoverflow.com/questions/6475314/python-for-in-loop-preceded-by-a-variable

#  design
'''
Innovation:
Fire projectile at mouse...
Create tiny healthbars above all mobs that adjust based on their hitpoints
Goals rules feedback freedom!!!


'''

# import libraries and modules
# from platform import platform
import pygame as pg
# import settings
# from settings import *
from pygame.sprite import Sprite
import random
from random import randint
import os
from math import *

import time

from time import *

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# sound added
pg.mixer.init

# game settings 
WIDTH = 360
HEIGHT = 480
FPS = 30
mpos = (0,0)

# player settings
PLAYER_GRAV = 0.9
PLAYER_FRIC = 0.1
SCORE = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

def colorbyte():
    return random.randint(0,255)

# create all classees as sprites...

# player sprite
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.r = 0
        self.g = 0
        self.b = 255
        self.image.fill((self.r,self.g,self.b))
        self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT-45)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
        self.jumppower = 10
    def controls(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.acc.y = -5
        if keys[pg.K_a]:
            self.acc.x = -5
        # if keys[pg.K_s]:
        #     self.acc.y = 5
        if keys[pg.K_d]:
            self.acc.x = 5
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -self.jumppower
    def draw(self):
        pass
    def inbounds(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        # self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.inbounds()
        self.rect.midbottom = self.pos

# platforms
class Platform(Sprite):
    def __init__(self, x, y, w, h, typeof):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.typeof = typeof
# powerup

class Powerup(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# display image
class Displayimage(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(GREEN)
        # self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        pass


# bullet sprite
class Pewpew(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.owner = ""
    def update(self):
        if self.owner == "player":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if (self.rect.y < 0):
            self.kill()
            print(pewpews)



# here's the healthbar
class Healthbar(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def damage(self, newwidth):
        self.rect.w = newwidth


# here's the mobs
class Mob(Sprite):
    def __init__(self, x, y, w, h, color, typeof, health):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.typeof = typeof
        self.health = health
        self.initialized = False
        self.healthbar = pg.Surface((self.rect.width, 5))
        self.healthbar.fill(RED)
    def update(self):
        # self.rect.x += self.speed
        self.rect.y += self.speed

        if self.typeof == "boss":
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speed *= -1
                self.rect.y += 15
        else:
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speed *= -1

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# instantiate classes
player = Player()
print(player.rect.x)
print(player.rect.y)
plat = Platform(180, 380, 100, 35, "normal")
plat2 = Platform(289, 180, 100, 35, "ouchie")
powerup1 = Powerup(100,350, 25, 25)
ground = Platform(0, HEIGHT-40, WIDTH, 40, "lava")
myimage = Displayimage(WIDTH/2, HEIGHT/2)

# create groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()
pewpews = pg.sprite.Group()
powerups = pg.sprite.Group()

# instantiate lots of mobs in a for loop and add them to groups
for i in range(30):
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (colorbyte(),colorbyte(),colorbyte()), "normal", 5)
    all_sprites.add(m)
    mobs.add(m)
    # print(m)

for i in range(2):
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT/3), 50, 50, (255,0,0), "boss", 25)
    all_sprites.add(m)
    mobs.add(m)
    # print(m)

# add things to groups...
all_sprites.add(player, plat, plat2, ground, myimage, powerup1)
powerups.add(powerup1)
all_plats.add(plat, plat2, ground)


############################# Game loop ###########################################
# starts timer...
start_ticks = pg.time.get_ticks()

running = True
while running:
    # keep the loop running using clock
    delta = clock.tick(FPS)
    seconds = floor((pg.time.get_ticks()-start_ticks)/1000)
    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        if hits[0].typeof == "ouchie":
            print("yikes I'm dead...")
        if hits[0].typeof == "lava":
            print("I'm standing on the LAVA...")
        if hits[0].typeof == "ouchie":
            print("yikes I'm dead...")
        # print("ive struck a plat")
        player.pos.y = hits[0].rect.top
        player.vel.y = 0

    for p in powerups:
        powerUphit = pg.sprite.spritecollide(player, powerups, True)
        if powerUphit:
            print("i got a powerup...")
            player.jumppower += 15

    for p in pewpews:
        mhit = pg.sprite.spritecollide(p, mobs, True)
        # print(mhit.keys())
        if mhit:
            mhit[0].health -= 1
            print("mob health is " + str(mhit[0].health))
            if mhit[0].health < 1:
                mhit[0].kill()
        # if mhit:
        #     print('hit mob ' + str(mhit[0]))
    
    mobhits = pg.sprite.spritecollide(player, mobs, True)

    if mobhits:
        # print("ive struck a mob")
        player.health -= 1
        if player.r < 255:
            player.r += 15 

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        # check for mouse
        if event.type == pg.MOUSEBUTTONUP:
            p = Pewpew(player.rect.midtop[0], player.rect.midtop[1], 10, 10)
            p.owner = "player"
            all_sprites.add(p)
            pewpews.add(p)
            mpos = pg.mouse.get_pos()
            print(mpos)
            # get a list of all sprites that are under the mouse cursor
            clicked_sprites = [s for s in mobs if s.rect.collidepoint(mpos)]
            for m in mobs:
                if m.rect.collidepoint(mpos):
                    print(m)
                    m.kill()
                    SCORE += 1

            # print(clicked_sprites)k 
        # check for keys
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()
        
    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ############ Draw ################
    # draw the background screen
      
    screen.fill(BLACK)
    # screen.fill(BLACK)

    # draw text
    draw_text("FPS: " + str(delta), 22, RED, 64, HEIGHT / 24)
    draw_text("Timer: " + str(seconds), 22, RED, 64, HEIGHT / 10)
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    draw_text("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
    # pg.draw.polygon(screen,BROWN,[(player.rect.x, player.rect.y), (152, 230), (1056, 230),(1056, 190)])
    
    # draw player color
    player.image.fill((player.r,player.g,player.b))

    
    # draw all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()
