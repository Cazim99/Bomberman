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
        
        self.images = ImageLoader.load(os.getcwd()+ "/Runner2D/data/game/map")
        for img in self.images:
            self.images[img] = pygame.transform.scale(self.images[img],(150,150))
            
        self.server_map = None
                
        self.player = Player(self.window, self.window.screen_size[0]/2, self.window.screen_size[1]/2, 0, 0 , 100, 130, "Cazim2")
        
     
    def move_map(self, x, y):
        self.map_position_x += x
        self.map_position_y += y
     
    def update(self):
        if self.playing:
            self.player.update()
        
    def render(self):
        if self.playing:
            
            self.window.screen.fill(pygame.Color('black'))
            
            # -------------- SERVER MAP -----------------
            
            if self.server_map != None:
                map_dp_copy = copy.deepcopy(self.server_map)
                for block in map_dp_copy:
                    self.window.screen.blit(self.images['wood'], block)
            # -------------- SERVER MAP -----------------
            
            
            self.player.render()
