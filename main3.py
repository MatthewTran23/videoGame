# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
import os

# setup asset folders here
game_folder= os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# game settings 
WIDTH = 360
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player class that uses sprite class to make an image and fill it red
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        # image fill red
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.xvel=5
        self.yvel=5
        print(self.rect.center)
    # do over and over again +5
    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if self.rect.x < 0:
            self.xvel*=-1
        if self.rect.y < 0:
            self.yvel*=-1
        if self.rect.x > WIDTH - self.rect.width:
            self.xvel*=-1
        if self.rect.y > HEIGHT - self.rect.height:
            self.yvel*=-1


# Player class that uses sprite class 
# class Player(Sprite):
#     def __init__(self):
#         Sprite.__init__(self)
#         self.image= pg.image.load(os.path.join(img_folder, 'Bell.jpg')).convert() 
#         # color key
#         self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.center = (WIDTH/2, HEIGHT/2)
#         self.xVel=5
#         self.yVel=5
#         print(self.rect.center)
#     # do over and over again +5
#     def update(self):
#         self.rect.x += self.xVel
#         self.rect.y += self.yVel
#         if (self.rect.x+50 > WIDTH):
#             self.xVel = -5
#         if self.rect.y < 0:
#             self.yVel = 5
#         if self.rect.x <0:
#             self.xVel=5
#         if self.rect.y > HEIGHT:
#             self.yVel=-5

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# create a group for all sprites, act on all sprites same time
all_sprites= pg.sprite.Group()

# instanciate the player
player = Player()

# add player to all sprites group
all_sprites.add(player)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    # Update all sprites
    all_sprites.update()

    # Draw the screen background 
    screen.fill(BLACK)

    # drall all sprites in the screen
    all_sprites.draw(screen)
    
    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()

