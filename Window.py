import pygame
pygame.init()
pygame.font.init()
from Mouse import Mouse
from GUI.Layout import AbsoluteLayout
from GUI.button import Button

from Game import Game

class Window:
    
    
    def __init__(self, width,height, window_name, dev_mode=True, fullscreen=False, sound=True, server=None):
        self.screen_size = (width,height) # dimenzije prozora
        self.window_name = window_name # ime prozora 
        self.game_running = False 
        self.dev_mode = dev_mode # za programera
        self.fullscreen = fullscreen
        self.sound = sound
        self.server = server
        self.reload = False
        
        # --- FPS ---
        self.FPS = 60
        self.FramePerSec = pygame.time.Clock()
        self.current_fps = self.FPS
        
         # Konstante
        self.FONT = pygame.font.SysFont("Bradley Hand ITC", int(self.screen_size[0]/50))
        self.BIG_FONT = pygame.font.SysFont("Bradley Hand ITC", int(self.screen_size[0]/50)+6)
        self.FONT_ARIAL = pygame.font.SysFont("Arial", int(self.screen_size[0]/50))
        self.FONT_BIG_ARIAL = pygame.font.SysFont("Arial", int(self.screen_size[0]/50)+6)
        
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.screen_size[0],self.screen_size[1]), pygame.NOFRAME) # postaviti prozor ali ne u fullscreen modu na osonovu dimenzija prozora (widht,height)
        pygame.display.set_caption(window_name) # postaviti ime prozora
        
        self.screen_size = (self.screen.get_width(), self.screen.get_height())
        
        self.mouse = Mouse(self, pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[0]) # Postavljanje misa na osnovu naseg odabira izgleda
        
        self.game = Game(self, server)
        
        # -------------- GUI ----------------------
        self.menu = AbsoluteLayout(self, 0, 0, self.screen_size[0], self.screen_size[1])
        self.play_btn = Button(self, self.screen_size[0]/2, self.screen_size[1]/2, text="PLAY", color="blue")
        self.menu.add_in_layout("play_btn", self.play_btn, hasEvent=True)
        self.settings_btn = Button(self, self.screen_size[0]/2, self.play_btn.rect.bottom + self.play_btn.rect.h + 60, text="SETTINGS", color="green")
        self.menu.add_in_layout("settings_btn", self.settings_btn, hasEvent=True)
        self.exit_btn = Button(self, self.screen_size[0]/2,self.settings_btn.rect.bottom + self.settings_btn.rect.h + 60, text="EXIT", color="red")
        self.menu.add_in_layout("exit_btn", self.exit_btn, hasEvent=True)
        
        self.settings = AbsoluteLayout(self, 0, 0, self.screen_size[0], self.screen_size[1], bg='stone')
        self.settings.hidden = True
        self.close_btn = Button(self, self.screen_size[0]/2, self.screen_size[1]/2, text="  ", color="cross")
        self.settings.add_in_layout("close_btn", self.close_btn, hasEvent=True)
        self.soundBtn = Button(self, self.screen_size[0]/2, self.close_btn.rect.bottom + self.close_btn.rect.h + 60, text="Sound off" if self.sound else "sound on", color="red" if self.sound else "green")
        self.settings.add_in_layout("sound_btn", self.soundBtn, hasEvent=True)
        self.FullScreenBtn = Button(self, self.screen_size[0]/2,self.soundBtn.rect.bottom + self.soundBtn.rect.h + 60, text="Fullscreen off" if self.fullscreen else "fullscreen on", color="red" if self.fullscreen else "green")
        self.settings.add_in_layout("fullscreen_btn", self.FullScreenBtn, hasEvent=True)
        
        
        
        if not self.sound:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
    
    #Metoda za zaustavljanje igrice
    def stop(self):
        print("[INFO] Game is closed")
        self.game_running = False
        
    #Metoda za pokretanje igrice
    def start(self):
        if self.game_running == True:
            print('[INFO] Game is allready running')
        else:
            self.game_running = True
            self.game_loop()
    
    def for_developer_game_info(self):
        if self.dev_mode == True:
            font = pygame.font.SysFont("Arial", int(self.screen_size[0]/100) * 2)
            fps_text = font.render(f"FPS: {int(self.current_fps)} x,y: {int(self.game.player.cam_x)}:{int(self.game.player.cam_y)} ROOM: {str(self.game.player.roomid)}", True, "red")
            self.screen.blit(fps_text, (10, 0))
       
    #Beskonacna petlja odrzavanje igre
    def game_loop(self):
        while self.game_running:
            self.update()
            self.render()
    
    #Metoda za pracenje bilo koje izmene na igrici
    def update(self):
        self.game.update()
        self.mouse.update()
        self.menu.update()
        self.settings.update()
        
    #Metoda za iscrtavanje
    def render(self):
        
        self.screen.fill(pygame.Color("black")) # postaviti belu pozadinu prozora
        
        self.game.render()
        
        # ---------------- zadnje uvek iscrtavaj ---------------- #
                
        self.menu.render()
        self.settings.render()
        self.mouse.render()
        
        
        self.for_developer_game_info() # za programera( mene )
        self.FramePerSec.tick(self.FPS) # FPS 
        self.current_fps = self.FramePerSec.get_fps() # Zapamti trenutni FPS
        pygame.display.update() # osveziti prozor iznova iscrtavanje
    
        