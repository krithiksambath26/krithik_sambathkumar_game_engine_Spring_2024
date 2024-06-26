#This file was created by Krithik Sambathkumar



import sys
import pygame as pg
from settings import *
from random import choice

vec = pg.math.Vector2

#Player Class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # added player image to sprite from the game class...
        self.image = game.player_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        
     

    
    #Player Controls
    def get_keys(self):
        self.vx, self.vy = 0, 0 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False

    # Collisions function     
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
     
    

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)

    # Backbone of Coint Counter and Timer functions
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "Mob":
                while True:
                    self.game.show_death_screen()
            if str(hits[0].__class__.__name__) == "Mob2":
                while True:
                    self.game.show_death_screen()
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                self.speed += 300
            if self.moneybag == 11:
               while True:
                    self.game.show_end_screen()
            if self.moneybag == 5:
                    self.game.start_new_game()



    def update(self):
 
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
 
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        if self.x < 0:
            self.x = 0
        elif self.x >= WIDTH:
            self.x = WIDTH-self.rect.width
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        if self.y < 0:
            self.y = 0
        elif self.y >= HEIGHT:
            self.y = HEIGHT-self.rect.height
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.mobs, True)
        self.collide_with_group(self.game.power_ups, True)
        
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")
# Wall Class     
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Second Wall Class
class Wall2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall2_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Coin Class
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Powerup Class
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.powerup_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Mob Class    
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 5
        
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y

    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        #To chase player
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

   #Second Boss Mob                  
class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob2_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1000

    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')



 

#____________________________________________________________________________________________
        
# class Mob(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.mobs
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         #self.image = game.mob_img
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(RED)
#         #self.image = self.game.mob_img
#         self.rect = self.image.get_rect()
#         self.hit_rect = MOB_HIT_RECT.copy()
#         self.hit_rect.center = self.rect.center
#         self.pos = vec(x, y) * TILESIZE
#         self.vel = vec(0, 0)
#         self.acc = vec(0, 0)
#         self.rect.center = self.pos
#         self.rot = 0
#         # added
#         self.speed = 1


#         # self.groups = game.all_sprites, game.mobs
#         # pg.sprite.Sprite.__init__(self, self.groups)
#         # self.game = game
#         # #self.image = game.Mob_img
#         # self.image = pg.Surface((TILESIZE, TILESIZE))
#         # self.image.fill(RED)
#         # self.rect = self.image.get_rect()
#         # self.x = x
#         # self.y = y
#         # self.vx, self.vy = 100, 100
#         # self.x = x * TILESIZE
#         # self.y = y * TILESIZE
#         # self.speed = 1
#         #self.chasing = False
#     def collide_with_walls(self, dir):
#         if dir == 'x':
#             # print('colliding on the x')
#             hits = pg.sprite.spritecollide(self, self.game.walls, False)
#             if hits:
#                 self.vx *= -3
#                 self.rect.x = self.x
#         if dir == 'y':
#             # print('colliding on the y')
#             hits = pg.sprite.spritecollide(self, self.game.walls, False)
#             if hits:
#                 self.vy *= -3
#                 self.rect.y = self.y
#     ##def sensor(self):
#         ##if self.rect.x - self.game.player.rect.x < 30 and self.rect.y - self.game.player.rect.y < 30:
#             ##self.chasing = True
#         ##else:
#             ##self.chasing = False
#     def update(self):

#         # self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
#         # # self.image = pg.transform.rotate(self.image, 45)
#         # # self.rect = self.image.get_rect()
#         # self.rect.center = self.pos
#         # self.acc = vec(self.speed, 0).rotate(-self.rot)
#         # self.acc += self.vel * -1
#         # self.vel += self.acc * self.game.dt
#         # self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
#         # # self.hit_rect.centerx = self.pos.x
#         # self.collide_with_walls(self, self.game.walls, 'x')
#         # self.hit_rect.centery = self.pos.y
#         # self.collide_with_walls(self, self.game.walls, 'y')
#         # self.rect.center = self.hit_rect.center
#         # # if self.health <= 0:
#         # #     self.kill()


#         # #if self.chasing:
#         # self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
#         # self.image = pg.transform.rotate(self.image, 45)
#         # self.rect = self.image.get_rect()
#         # self.rect.center = self.pos
#         # self.acc = vec(self.speed, 0).rotate(-self.rot)
#         # self.acc += self.vel * -1
#         # self.vel += self.acc * self.game.dt
#         # self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
#         # self.hit_rect.centerx = self.pos.x
#         # collide_with_walls(self, self.game.walls, 'x')
#         # self.hit_rect.centery = self.pos.y
#         # collide_with_walls(self, self.game.walls, 'y')
#         # self.rect.center = self.hit_rect.center
#         # if self.health <= 0:
#         #     self.kill()
        
        
        
        
        
        
        
        
        
#        # if self.chasing:
            
#         # self.rect.x += 1
#         # self.x += self.vx * self.game.dt
#         # self.y += self.vy * self.game.dt
        
#         # if self.rect.x < self.game.player.rect.x:
#         #     self.vx = 100
#         # if self.rect.x > self.game.player.rect.x:
#         #     self.vx = -100    
#         # if self.rect.y < self.game.player.rect.y:
#         #     self.vy = 100
#         # if self.rect.y > self.game.player.rect.y:
#         #     self.vy = -100
#         # self.rect.x = self.x
#         # self.collide_with_walls('x')
#         # self.rect.y = self.y
#         # self.collide_with_walls('y')