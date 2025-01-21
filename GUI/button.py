import pygame
from pygame import mixer
import Window
from ImageLoader import ImageLoader
import os
from _thread import *
import time


class Button:

    def __init__(self, window: 'Window.Window', x, y, text, color, text_color="white", useAsX=False):
        self.window = window
        self.id = text
        self.useAsX = useAsX

        self.click_channel = pygame.mixer.Channel(6)
        self.click_sound = mixer.Sound(f"{os.getcwd()}/Bomberman/data/sounds/click-b.ogg")
        
        self.color = color
        self.text = window.FONT_ARIAL.render(f"{text}", True, text_color)

        self.disabled = False
        self.pressedElement = False

        self.images = ImageLoader.load(f"{os.getcwd()}/Bomberman/data/gui_images/button")
        self.images[self.color + '_btn'] = pygame.transform.scale(self.images[self.color + '_btn'],((window.FONT.get_height()*2)+(self.text.get_width()*3), window.FONT.get_height()*4))
        self.images[self.color + '_btn_pressed'] = pygame.transform.scale(self.images[self.color + '_btn_pressed'],((window.FONT.get_height()*2)+(self.text.get_width()*3), window.FONT.get_height()*4))
        self.images[self.color + '_btn_hover'] = pygame.transform.scale(self.images[self.color + '_btn_hover'],((window.FONT.get_height()*2)+(self.text.get_width()*3), window.FONT.get_height()*4))
        self.current_image = self.images[self.color + '_btn']
        self.hoverImage = self.images[self.color + '_btn_hover']
        
        self.x = x
        self.y = y

        self.rect = pygame.Rect(0, 0, self.images[self.color + '_btn'].get_width(), self.images[self.color + '_btn'].get_height())
        self.rect.center = [x, y]
        

    def pressed(self):
        if not self.click_channel.get_busy() and self.disabled == False:
            self.click_channel.play(self.click_sound)
        self.current_image = self.images[self.color + '_btn_pressed']
        self.pressedElement = True
        self.unpressed()

    def timer(self):
        time.sleep(0.4)
        self.current_image = self.images[self.color + '_btn']
        self.pressedElement = False

    def unpressed(self):
        start_new_thread(self.timer,())

    def render(self):
        if not self.disabled:
            self.window.screen.blit(self.current_image, self.rect)
            self.window.screen.blit(self.text, (self.rect.center[0] - self.text.get_width()/2, self.rect.center[1] - self.text.get_height()/2))
