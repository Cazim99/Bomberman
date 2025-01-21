import pygame
import os

class ImageLoader:
    
    @staticmethod
    def load(location):
        images = {}
        for img in os.listdir(location):
            if img.endswith(".png"):
                 image = pygame.image.load(location + os.sep + img).convert_alpha()
                 images[str(img).replace(".png", "")] = image
        return images