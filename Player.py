import pygame
from ImageLoader import ImageLoader
import os
from Client import Client
import copy

class Player:
    
    
    def __init__(self,window, x, y,camx, camy, width, height, name):
        self.window = window
        self.x = x
        self.y = y
        self.roomid = None
        self.cam_x = camx
        self.cam_y = camy
        self.widht = width
        self.height = height
        self.name = name
        self.initalized = False
        self.other_players_data = {}
        self.bomb_id = 0
        
        self.data = {
            'username':self.name,
            'cordinates':(self.cam_x,self.cam_y),
            'width':self.widht,
            'height':self.height,
            'roomid':self.roomid,
            'initalized':self.initalized,
        }
        
        
        self.rect = pygame.Rect(0,0,width,height)
        self.rect.center = [x,y]
        
        
        self.images = ImageLoader.load(os.getcwd()+"/Bomberman/data/Player")
        
        self.right_walk_list_name = ("11","12","13")
        self.right_walk = []
        self.left_walk_list_name = ("14","15","16")
        self.left_walk = []
        self.up_walk_list_name = ("02","03","04")
        self.up_walk = []
        self.down_walk_list_name = ("23","24","01")
        self.down_walk = []
        
        
        for img in self.images:
            self.images[img] = pygame.transform.scale(self.images[img],(width,height))
        
        for img in self.images:
            if str(img).endswith(self.right_walk_list_name):
                self.right_walk.append(self.images[img])
            elif str(img).endswith(self.left_walk_list_name):
                self.left_walk.append(self.images[img])
            elif str(img).endswith(self.up_walk_list_name):
                self.up_walk.append(self.images[img])
            elif str(img).endswith(self.down_walk_list_name):
                self.down_walk.append(self.images[img])
        
        self.idle_image = self.images["player_23"]
        
        self.mask = pygame.mask.from_surface(self.idle_image)
        
        # ANIMATION
        self.current_image = self.idle_image
        self.facing_left = False
        self.anim = [self.idle_image]
        self.anim_index = 0 
        self.anim_speed = 5
        self.animation_colldown = 0 
        self.move_speed = 10
     
    """def collision(self, rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False"""
    
    def collision(self, other):
        offset = (other.x - self.rect.x, other.y - self.rect.y)
        other_mask = pygame.mask.from_surface(self.window.game.images['wood'])
        return self.mask.overlap(other_mask, offset) is not None    
    
    def calculate_cords_by_my_position(self, cordinates):
        
        new_x = cordinates[0] + self.rect.center[0] - self.cam_x
        new_y = cordinates[1] + self.rect.center[1] - self.cam_y
        return [new_x, new_y]    
    
    def render_other_players(self):
        try:
            if 'users' in self.other_players_data:
                users = self.other_players_data['users']
                for player in users:
                    if users[player]['username'] != self.name:
                        cords = self.calculate_cords_by_my_position((self.other_players_data['users'][player]['cordinates'][0], self.other_players_data['users'][player]['cordinates'][1]))
                        rect = pygame.Rect(0, 0, self.other_players_data['users'][player]['width'], self.other_players_data['users'][player]['height'])
                        rect.center = [cords[0], cords[1]]
                        self.window.screen.blit(self.idle_image, rect)
        except Exception as ex:
            print(ex)
            
            
    def update(self):
        if self.window.game.playing == True:
            self.keyboard_events()
            self.update_animation()
            self.data = {
                'username':self.name,
                'cordinates':(self.cam_x,self.cam_y),
                'width':self.widht,
                'height':self.height,
                'roomid':self.roomid,
                'initalized':self.initalized,
            }
            self.window.game.internet.send_to_server(self.data)
     
    def update_animation(self):
        if self.animation_colldown >= self.anim_speed:
            self.animation_colldown = 0
            self.anim_index += 1
            if self.anim_index >= len(self.anim): 
                self.anim_index = 0
                    
            self.current_image = self.anim[self.anim_index]
        self.animation_colldown += 1 
    
    def keyboard_events(self):        
        if self.window.game.server_map != None:
            key_pressed = pygame.key.get_pressed()
        
            if True not in key_pressed:
                self.anim = [self.idle_image]

            if key_pressed[pygame.K_d]:
                self.facing_left = False
                self.anim = self.right_walk
                self.window.game.move_map(-self.move_speed,0)
                self.cam_x += self.move_speed
                for n in self.window.game.server_map:
                    if self.collision(n):
                        self.window.game.move_map(self.move_speed,0)
                        self.cam_x += -self.move_speed
                    

            
            if key_pressed[pygame.K_s]:
                self.facing_left = False
                self.anim = self.down_walk
                self.window.game.move_map(0,-self.move_speed)
                self.cam_y += self.move_speed
                for n in self.window.game.server_map:
                    if self.collision(n):
                        self.window.game.move_map(0,self.move_speed)
                        self.cam_y += -self.move_speed

                
            if key_pressed[pygame.K_w]:
                self.facing_left = False
                self.anim = self.up_walk
                self.window.game.move_map(0,self.move_speed)
                self.cam_y += -self.move_speed
                for n in self.window.game.server_map:
                    if self.collision(n):
                        self.window.game.move_map(0,-self.move_speed)
                        self.cam_y += self.move_speed

    
                        
            
            if key_pressed[pygame.K_a]:
                self.facing_left = True
                self.anim = self.left_walk
                self.window.game.move_map(self.move_speed,0)
                self.cam_x += -self.move_speed
                for n in self.window.game.server_map:
                    if self.collision(n):
                        self.window.game.move_map(-self.move_speed,0)
                        self.cam_x += self.move_speed
                        
            if key_pressed[pygame.K_SPACE]:
                self.data = {
                    'username':self.name,
                    'cordinates':(self.cam_x,self.cam_y),
                    'width':self.widht,
                    'height':self.height,
                    'roomid':self.roomid,
                    'initalized':self.initalized,
                    'bomb_id':self.bomb_id,
                    'bomb':(self.cam_x,self.cam_y),
                }
                self.window.game.internet.send_to_server(self.data)

    
    def render(self):
        if self.window.game.playing == True:
            self.render_other_players()
            if self.window.game.playing == True:
                self.window.screen.blit(self.current_image, self.rect)
                pygame.draw.rect(self.window.screen, "red", self.rect, 1)
        