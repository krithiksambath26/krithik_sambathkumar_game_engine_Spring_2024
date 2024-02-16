# This file was created by Krithik S

# Importing Libaries
import pygame as pg
from settings import *
from sprites import *
import sys
from random import randint
from os import path

# Creating a Game Class
class Game:
     # Definig what is in the class
    def __init__(self):
        pg.init()
        # Creating dimensions for game's graphic display 
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
         # Making a title for the game 
        pg.display.set_caption("My First Video Game")
        #Creating a time for the display to show
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
    
        #Will eventually store game info with this
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
    # With is context manager which prevents errors
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)


    def new(self):
        
        #Creating variables 
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.object2s = pg.sprite.Group()
        
        #self.player = Player(self, 10, 10)
        #self.all_sprites.add(self.player)
    
    
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'X':
                    object2(self, col ,row)

    #Used to run game 
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # This is input
            self.events()
            # This is the processing
            self.update()
            # This is the output (Drawings, sound, etc)
            self.draw()
        

    def quit(self):
        pg.quit()
        sys.exit()
     #method (kinda like function)
    def input(self): 
        pass
    def update(self):
        self.all_sprites.update()
    #To draw playing field 
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
             pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range (0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    def events(self):
            for event in pg.event.get():
                # when you hit the red x the window closes the game ends
                if event.type == pg.QUIT:
                    self.quit()
                    print("the game has ended..")
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.player.move(dx=-1)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        self.player.move(dx=1)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.player.move(dy=-1)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        self.player.move(dy=1)
    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

   

#running the game
    
g = Game()
# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()