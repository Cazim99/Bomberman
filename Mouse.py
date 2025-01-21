import pygame
from ImageLoader import ImageLoader
import os
from GUI.button import Button
import time
class Mouse:
    
    def __init__(self, window, x, y):
        self.window = window # prozor na koji ce mis biti koriscen
        self.pos = [x,y] # pozicija misa
        pygame.mouse.set_visible(False) # sakri default mis
        
        self.mouse_images = ImageLoader.load(os.getcwd() + "/Runner2D/data/cursor") # ucitavanje slika misa
        self.current_mouse_image = self.mouse_images['cursor'] # postavljanje prvobitne slike kada je mis u staticnom stanju
        
        self.rect = self.current_mouse_image.get_rect() 
    
    def mouse_hover(self):
        self.current_mouse_image = self.mouse_images['cursor_click']
    
    def mouse_unhover(self):
        self.current_mouse_image = self.mouse_images['cursor']
     
    def update(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.rect.center = [self.x,self.y]
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.window.menu.hidden == False:
                    elements = self.window.menu.elements
                    for key in elements:
                        if elements[key]['hasEvent']:
                            if elements[key]['element'].rect.colliderect(self.rect):
                                elements[key]['element'].pressed()
                                if key == "play_btn" and elements[key]['element'].disabled == False:
                                    self.window.game.playing = True
                                    self.window.menu.hidden = True
                                    self.window.settings.hidden = True
                                    self.window.game.internet.connect_to_server()
                                elif key == "settings_btn" and elements[key]['element'].disabled == False:
                                    self.window.menu.hidden = True
                                    self.window.settings.hidden = False
                                elif key == "exit_btn" and elements[key]['element'].disabled == False:
                                    self.window.game.internet.disconnect()
                                    time.sleep(1)
                                    self.window.stop()
                                else:
                                    pass
                                break
                elif self.window.settings.hidden == False:
                    elements = self.window.settings.elements
                    for key in elements:
                        if elements[key]['hasEvent']:
                            if elements[key]['element'].rect.colliderect(self.rect):
                                elements[key]['element'].pressed()
                                if key == "close_btn" and elements[key]['element'].disabled == False:
                                    self.window.menu.hidden = False
                                    self.window.settings.hidden = True
                                elif key == "sound_btn" and elements[key]['element'].disabled == False:
                                    if self.window.sound == True:
                                        self.window.sound = False
                                    else:
                                        self.window.sound = True
                                        
                                    if not self.window.sound:
                                        pygame.mixer.pause()
                                    else:
                                        pygame.mixer.unpause()
                                    self.window.settings.elements[key]['element'] = Button(self.window, self.window.screen_size[0]/2, self.window.close_btn.rect.bottom + self.window.close_btn.rect.h + 60, text="Sound off" if self.window.sound else "sound on", color="red" if self.window.sound else "green")
                                elif key == "fullscreen_btn" and elements[key]['element'].disabled == False:
                                    self.window.reload = True
                                    if self.window.fullscreen == True:
                                        self.window.fullscreen = False
                                    else:
                                        self.window.fullscreen = True
                                    self.window.stop()
                                else:
                                    pass
                                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.window.menu.hidden = False
                    self.window.settings.hidden = True
            
    def render(self):
        self.window.screen.blit(self.current_mouse_image, self.rect)