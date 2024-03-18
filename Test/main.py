# This file was created by Krithik Sambathkumar person

#Game Goals:
# Boss level, Collecting Coins, Start - End screen
# 8 bit Venom Chasing player before player collects coins

# Importing Libaries

import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

from math import floor

# Timer Class
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
        #images folder and images in the load_data method for use with the player
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'venom.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, 'carnage.png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, 'floor1.png')).convert_alpha()
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

        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
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
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, "Time " + str(self.test_timer.countdown(45)), 24, BLACK, WIDTH/2 - 32, 2)
            self.draw_text(self.screen, "Score " + str (self.player.moneybag),24, BLACK, WIDTH/2 - 32,30)
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

g = Game()

while True:
    g.new()
    g.run()



#C = coin
#1 = wall
#P = player
#U = Powerup
#. = empty space
#M = mob