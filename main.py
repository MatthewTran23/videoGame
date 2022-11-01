# Souces:
# shorthand for loops (used in getting mouse collision with sprite): https://stackoverflow.com/questions/6475314/python-for-in-loop-preceded-by-a-variable
# Ryan Deivert Class of 2023 THE BEST(Aided with bugs in code and genral knowledge)
# https://www.w3schools.com/python/python_variables_global.asp
# Clear Code Video on General Knowledge Pygame Platformers: https://www.youtube.com/watch?v=YWN8GcmJ-jA
# Pygame Docs: https://www.pygame.org/docs/

'''
Goals:

Built in functions, modules, Variables, Operators, Lists, If...Else statements, loops, and functions, Classes, and the pygame library.

Using the existing code base, you should innovate on the design.

Game should clearly have goals, rules, feedback, and freedom.

Code should include comments for each block of code.  Comments should be concise but informative.  All sources should be cited.

Create Simple Platformer

Goal game player reach top platform

Death functionality

Win display

Death Display

Mob Interactions with health

'''

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

# short hand for pygame vector for ease of use
vec = pg.math.Vector2


# game settings 
WIDTH = 500
HEIGHT = 720
FPS = 30
mpos = (0,0)

# player settings
PLAYER_GRAV = 0.9

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# function for display text on screen
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# returns random rgb value
def colorbyte():
    return random.randint(0,255)

# class to create display screen for rules
class Startscreen(Sprite):
    # attribute for class
    def __init__(self):
        Sprite.__init__(self)
        self.rect = pg.Rect(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT)
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.isalive= True
    # method check key press to remove startscreen
    def checkclick(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.isalive = False
    # method that displays text on start screen
    def display(self):
        draw_text("Jump to the Top Platform to win, Dodge Mobs and Don't Fall", 18, BLACK, WIDTH/2, HEIGHT / 2- 50)
        draw_text("SPACE to start", 18, BLACK, WIDTH/2, (HEIGHT /2)+50)
    # method draw background 
    def draw(self):
        if self.isalive == True:
            pg.draw.rect(screen, (255,255,255), self.rect)
            self.display()
    # update method 
    def update(self):
        self.checkclick()

# Player sprite for player functionality and update
class Player(Sprite):
    # attribute of class
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
    # method for controls for player
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
    # jump method 
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -17
    # inbound method to keep display
    def inbounds(self):
        if self.pos.x < 0:
            self.pos.x = 0+ 25
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH-25
     # update method
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        self.inbounds()
        

# platforms class
class Platform(Sprite):
    # attribute of class
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# mobns class
class Mob(Sprite):
    # attribute of class
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
    # update method
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.x < 0:
            self.speed *= -1
        

# init pygame and create a window
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# create groups for sprites
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate classes
startscreen= Startscreen()
player = Player()
ground = Platform(0, HEIGHT-20, 100, 20)
plat = Platform(100, HEIGHT-150, 100, 20)
plat2 = Platform(300, HEIGHT-90, 100, 20)
plat3 = Platform(500, HEIGHT-170, 100, 20)
plat4 = Platform(WIDTH-20, HEIGHT-260, 20, 20)
plat5 = Platform(WIDTH-180, HEIGHT-350, 100, 20)
plat6 = Platform(WIDTH-20, HEIGHT-520, 20, 20)
plat7 = Platform(0, HEIGHT-450, 100, 20)
plat8 = Platform(150, HEIGHT-600, 40, 20)
plat9 = Platform(210 , 40, 100, 20)

# create mobs on random positions and colors
for i in range(20):
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT-100), 25, 25, (colorbyte(),colorbyte(),colorbyte()))
    all_sprites.add(m)
    mobs.add(m)

# add instances to respetive groups
all_sprites.add( player, plat, plat2,plat3, plat4, plat5, plat6, plat7, plat8, plat9, ground)
all_plats.add(plat, plat2,plat3, plat4, plat5, plat6, plat7, plat8, plat9, ground)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)
    # if statment for player rect collide with mobs, kills mob and hurts player
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        player.health -= 5
        if player.r < 255:
            player.r += 15 
    # if statment for player rect collide with all_plats
    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        player.pos.y = hits[0].rect.top
        player.vel.y = 0
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        # check for mouse
        if event.type == pg.MOUSEBUTTONUP:
            mpos = pg.mouse.get_pos()
            # print(mpos)
            # get a list of all sprites that are under the mouse cursor
            clicked_sprites = [s for s in mobs if s.rect.collidepoint(mpos)]
            for m in mobs:
                if m.rect.collidepoint(mpos):
                    m.kill()
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
    startscreen.update()
    startscreen.draw()

    # draw lose text with if conditions
    draw_text("HEALTH: " + str(player.health), 22, WHITE, 90, HEIGHT / 24)
    if player.health <= 0 or player.rect.y > HEIGHT :
        draw_text("YOU LOSE", 50, RED, WIDTH / 2, 320)
        player.kill()
    # draw win screen with if conditions
    if player.rect.y < 20 and player.rect.x > 210 and player.rect.x < 310:
        draw_text("YOU WIN", 50, BLUE, WIDTH / 2, 320)
        player.kill()
        
    # draw player color
    player.image.fill((player.r,player.g,player.b))

    # draw all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()