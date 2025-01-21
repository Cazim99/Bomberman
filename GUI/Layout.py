import pygame
from ImageLoader import ImageLoader
import os
from _thread import *

class AbsoluteLayout:
    
    
    def __init__(self,window, x,y, width, height, bg='grass'):
        self.window = window
        self.pos = [x,y] # pozicija layouta
        self.size = [width,height] # sirina visina layouta
        
        self.margin = 0
        self.hidden = False
        
        self.rect = pygame.Rect(self.pos[0] + self.margin, self.pos[1] + self.margin, self.size[0] - self.margin*2,self.size[1] - self.margin*2)
        
        self.sponsor = pygame.image.load(f"{os.getcwd()}/Bomberman/data/Kenny.png")
        self.sponsor2 = pygame.image.load(f"{os.getcwd()}/Bomberman/data/zc.png")
        
        self.layout_images = ImageLoader.load(os.getcwd() + "/Bomberman/data/Layout")
        self.layout_images['grass'] = pygame.transform.scale(self.layout_images['grass'], (self.size[0]-self.margin*2, self.size[1]-self.margin*2))
        self.layout_images['stone'] = pygame.transform.scale(self.layout_images['stone'], (self.size[0]-self.margin*2, self.size[1]-self.margin*2))
        
        self.current_bg = self.layout_images[bg]
        
        self.elements = {}
        
      
    def add_in_layout(self, key, element, hasEvent = False):
        self.elements[key] = {'element':element, 'hasEvent':hasEvent}
        
    def mouse_events(self):
        if self.hidden == False:
            # ------------ MOUSE HOVER EVENT CHAINGING CURRSOR 
            mouse_hover_element = False
            for key in self.elements:
                if self.elements[key]['hasEvent'] == True:
                    if self.window.mouse.rect.colliderect(self.elements[key]['element'].rect):
                        mouse_hover_element = True
                        self.window.cursor = self.window.mouse.mouse_hover()
                        if self.elements[key]['element'].pressedElement == False:
                            self.elements[key]['element'].current_image = self.elements[key]['element'].images[self.elements[key]['element'].color + '_btn_hover']
                        break
                            
            if mouse_hover_element == False:
                self.window.cursor = self.window.mouse.mouse_unhover()
                
            for key in self.elements:
                if self.elements[key]['hasEvent'] == True:
                    if not self.window.mouse.rect.colliderect(self.elements[key]['element'].rect):
                        if self.elements[key]['element'].pressedElement == False:
                            self.elements[key]['element'].current_image = self.elements[key]['element'].images[self.elements[key]['element'].color + '_btn']
            # ------------ MOUSE HOVER EVENT CHAINGING CURRSOR   
    
    def update(self):
        if self.hidden == False:
            self.mouse_events()
        
    def render(self):
        if self.hidden == False:
            self.window.screen.blit(self.current_bg, self.rect)
            for key in self.elements:
                    self.elements[key]['element'].render()
                    
            self.window.screen.blit(self.sponsor, (self.size[0]-self.sponsor.get_width()-10,self.size[1]-self.sponsor.get_height()-10))
            self.window.screen.blit(self.sponsor2, (0,self.size[1]-self.sponsor2.get_height()))
        
        