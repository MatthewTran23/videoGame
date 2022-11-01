# content from kids can code: http://kidscancode.org/blog/

# sources
# getting mouse position: https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.get_pos
# shorthand for loops (used in getting mouse collision with sprite): https://stackoverflow.com/questions/6475314/python-for-in-loop-preceded-by-a-variable

#  design
'''
Goals:

Built in functions, modules, Variables, Operators, Lists, If...Else statements, loops, and functions, Classes, and the pygame library.

Using the existing code base, you should innovate on the design.

Game should clearly have goals, rules, feedback, and freedom.

Code should include comments for each block of code.  Comments should be concise but informative.  All sources should be cited.

make platform friction like ice

spikes from vector art


'''

# import libraries and modules
# from platform import platform
from pickle import FALSE
from turtle import width
import pygame as pg
# import settings
# from settings import *
from pygame.sprite import Sprite
import random
from random import randint

vec = pg.math.Vector2


# game settings 
WIDTH = 1080
HEIGHT = 720
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

# sprites...
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((25, 25))
        self.r = 0
        self.g = 0
        self.b = 255
        self.image.fill((self.r,self.g,self.b))
        self.rect = self.image.get_rect()
        self.rect.center = (45, HEIGHT-25)
        self.pos = vec(45, HEIGHT-25)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
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
            self.vel.y = -17
    def draw(self):
        pass
    def move_and_collide(self, dx, dy, group):
        self.rect.x += dx  # type: ignore
        hit_list = pg.sprite.spritecollide(self, group, False)
        for tile in hit_list:
            if dx > 0: # Moving right; Hit the left side of the wall
                self.rect.right = tile.rect.left
            if dx < 0: # Moving left; Hit the right side of the wall
                self.rect.left = tile.rect.right
        self.rect.y += dy  # type: ignore
        hit_list = pg.sprite.spritecollide(self, group, False)
        for tile in hit_list:
            if dy > 0: # Moving down; Hit the top side of the wall
                self.rect.bottom = tile.rect.top
            if dy < 0: # Moving up; Hit the bottom side of the wall
                self.rect.top = tile.rect.bottom
    def update(self):
            self.acc = vec(0,PLAYER_GRAV)
            self.controls()
            self.acc.x += self.vel.x * -0.1
            self.vel += self.acc
            self.rect.midbottom = self.pos
# platforms
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Healthbar(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.x < 0:
            self.speed *= -1
        

# init pygame and create a window
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# create groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate classes
player = Player()
plat = Platform(0, HEIGHT-150, WIDTH-120, 20)
plat2 = Platform(120, HEIGHT-280, WIDTH, 20)
plat3=Platform(0, HEIGHT-410, WIDTH-120, 20)
plat4 = Platform(120, HEIGHT-540, WIDTH, 20)
wallleft = Platform(0, 0, 20, 720)
wallright= Platform(WIDTH-20, 0, 20, 720)
ground = Platform(0, HEIGHT-20, WIDTH, 20)


for i in range(30):
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (colorbyte(),colorbyte(),colorbyte()))
    all_sprites.add(m)
    mobs.add(m)
# add things to groups...
all_sprites.add(player, plat, plat2,plat3,plat4, wallleft,wallright, ground)
all_plats.add(plat, plat2,plat3, plat4, wallleft,wallright, ground)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        # print("ive struck a mob")
        player.health -= 1
        if player.r < 255:
            player.r += 15
    player.move_and_collide(player.vel.x, player.vel.y, all_plats) 
    print(player.vel)
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        # check for mouse
        if event.type == pg.MOUSEBUTTONUP:
            mpos = pg.mouse.get_pos()
            # get a list of all sprites that are under the mouse cursor
            clicked_sprites = [s for s in mobs if s.rect.collidepoint(mpos)]
            for m in mobs:
                if m.rect.collidepoint(mpos):
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
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    draw_text("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
    # pg.draw.polygon(screen,BLUE,[(player.rect.x, player.rect.y), (152, 230), (1056, 230),(1056, 190)])
    
    # draw player color
    player.image.fill((player.r,player.g,player.b))

    
    # draw all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()