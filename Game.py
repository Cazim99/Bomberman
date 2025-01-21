import pygame
from ImageLoader import ImageLoader
import os
from Player import Player
from Client import Client
import copy
class Game:
    
    
    def __init__(self, window, server, playing=False):
        self.window = window
        self.playing = playing
        
        self.server = server
        self.internet = Client(self)
    
        self.map_width = 10 * 150
        self.map_height = 10 * 150
        self.map_position_x = ((self.window.screen_size[0] / 2) - (self.map_width / 2))
        self.map_position_y = ((self.window.screen_size[1] / 2) - (self.map_height / 2)) 
        
        self.images = ImageLoader.load(os.getcwd()+ "/Bomberman/data/game/map")
        for img in self.images:
            self.images[img] = pygame.transform.scale(self.images[img],(150,150))
            
        self.server_map = None
        self.server_map_desing = None
        self.bombs = {}
                
        self.player = Player(self.window, self.window.screen_size[0]/2, self.window.screen_size[1]/2, 0, 0 , 100, 130, "Cazim")
        
     
    def move_map(self, x, y):
        for block in self.server_map:
            block.x += x
            block.y += y
     
    def update(self):
        if self.playing:
            self.player.update()
        
    def render(self):
        if self.playing:
            
            self.window.screen.fill(pygame.Color('black'))
            
            # -------------- SERVER MAP -----------------
            
            if self.server_map != None:
                map_dp_copy = copy.deepcopy(self.server_map)
                
                # --- FLOOR ---
                x = self.server_map[0].x
                y = self.server_map[0].y
                c = 0
                for floor_block in self.server_map_desing:
                    self.window.screen.blit(self.images['ground'], pygame.Rect(x,y,150,150))
                    x += 150
                    c += 1
                    if c >= 10:
                        x = self.server_map[0].x
                        y += 150
                        c = 0
                
                
                for index,block in enumerate(map_dp_copy):
                    if self.server_map_desing[index] == '1':
                        pass
                    elif self.server_map_desing[index] == '0':
                        self.window.screen.blit(self.images['wood'], block)
                    elif self.server_map_desing[index] == '#':
                        self.window.screen.blit(self.images['metal'], block)
            # -------------- SERVER MAP -----------------
            
            
            # -------------- BOMBS -----------------
            for bomb in self.bombs:
                pygame.draw.rect(self.window.screen,"red", (self.bombs[bomb][0][0],self.bombs[bomb][0][1],50,50),1)
            # -------------- BOMBS -----------------
            
            
            self.player.render()
