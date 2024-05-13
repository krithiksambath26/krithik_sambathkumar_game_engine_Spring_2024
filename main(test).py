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


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.current_level = 0  # Start with level 0
        self.load_data()

    def load_data(self):
        # Load images and other resources
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.background_img = pg.image.load(path.join(img_folder, 'bg.png')).convert_alpha()
        self.player_img = pg.image.load(path.join(img_folder, 'spiderman.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, 'carnage.png')).convert_alpha()
        self.mob2_img = pg.image.load(path.join(img_folder, 'venom(BIG).png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, 'floor4.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(img_folder, 'coin.png')).convert_alpha()
        self.powerup_img = pg.image.load(path.join(img_folder, 'powerup.png')).convert_alpha()

        # Load level data
        self.load_level()

    def load_level(self):
        level_file = f"level{self.current_level + 1}.txt"  # Assumes level files are named level1.txt, level2.txt, etc.
        game_folder = path.dirname(__file__)
        with open(path.join(game_folder, level_file), 'rt') as f:
            self.map_data = [line.strip() for line in f]

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()

        # Load entities based on the current level data
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'm':
                    Mob2(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'C':
                    Coin(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)
                elif tile == 'U':
                    PowerUp(self, col, row)

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background_img, (0, 0))
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def start_new_level(self):
        self.current_level += 1
        if self.current_level < MAX_LEVELS:
            self.load_level()
            self.new()
        else:
            self.show_end_screen()

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def show_end_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You completed all levels! Press any key to exit", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
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
    

