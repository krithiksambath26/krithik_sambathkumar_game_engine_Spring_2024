# This file was created by Krithik Sambathkumar 

#Game Goals:
# 3 Features: Coin Counter (Done), Added graphics (DONE), Coin counter, Timer (Done)

# 8 bit Venom and other enemies chasing player before player collects coins

# 1 Design Goal (BETA): Add working Start, End, and Death screens

# Current: Beta Build


import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

from math import floor

# Added Timer Class 
class Cooldown():
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)


#Class Game
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        #images folder; calling folder to use imported png's with mobs
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.background_img = pg.image.load(path.join(img_folder, 'bg.png')).convert_alpha()
        self.background_rect = self.background_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, 'spiderman.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, 'carnage.png')).convert_alpha()
        self.mob2_img = pg.image.load(path.join(img_folder, 'venom(BIG).png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, 'floor4.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(img_folder, 'coin.png')).convert_alpha()
        self.powerup_img = pg.image.load(path.join(img_folder, 'powerup.png')).convert_alpha()
        self.map_data = []
        
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    def new(self):
        self.test_timer = Cooldown()
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()

        #Assing Mobs and Walls a symbol to correlate to map
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'm':
                    Mob2(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)

    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()

    def update(self):
        self.test_timer.ticking()
        self.all_sprites.update()
    
    #Creating the Playing Screen
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    #Text Settings
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    
    #Instantiating Game Screen
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.screen.blit(self.background_img, self.background_rect)
            # game_folder = path.dirname(__file__)
            # img_folder = path.join(game_folder, 'images')
            # self.screen = pg.image.load(path.join(img_folder, 'bg.png')).convert_alpha()
            #self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, "Time " + str(self.test_timer.countdown(45)), 24, WHITE, WIDTH/2 - 32, 2)
            self.draw_text(self.screen, "Score " + str (self.player.moneybag),24, WHITE, WIDTH/2 - 32,30)
            pg.display.flip()



    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)

    # Start Screen Function            
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
        
    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the GO screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def show_end_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You Won! - press any X to exit", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def show_death_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You Died! - press any X to exit", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
        

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

g = Game()

g.show_start_screen()

while True:
    g.new()
    g.run()



# Letter assignments per Enitity: 
    
#C = coin
#1 = wall
#m = wall2
#P = player
#U = Powerup
#. = empty space
#M = mob
    

