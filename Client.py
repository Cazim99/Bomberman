import socket
import pickle
import threading
import time
import os
import pygame

class Client(threading.Thread):
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(4) # If reciving data from server take more then 4 secounds try reconnecting 
    BYTES_LEN = 3072
    
    running = True
    freez_game = True
    
    def __init__(self, game):
        self.game = game
        self.serverAddress = (self.game.server[0], self.game.server[1])
        super().__init__(target="run", daemon=True)
        
    def run(self):
        self.send_to_server(self.game.player.data)
        while self.running:
            try:
                data_from_server = self.recive_from_server()['data']['users']
                self.game.player.other_players_data = data_from_server
                self.game.player.roomid = data_from_server['users'][self.game.player.name]['roomid']
                if 'users' in data_from_server:
                    myself = data_from_server['users'][self.game.player.data['username']]
                    
                    # --------- LOADING MAP ------------ 
                    map = []
                    map_desing = data_from_server['map']
                    x = self.game.map_position_x
                    y = self.game.map_position_y
                    c = 0
                    for block in map_desing:
                        if block != '1':
                            map.append(pygame.Rect(x,y,150,150))
                        x += 150
                        c += 1
                        if c >= 10:
                            x = self.game.map_position_x
                            y += 150
                            c = 0
                        
                    self.game.server_map = map
                    # --------- LOADING MAP ------------ 
                    
                    if 'new_cordinates' in myself:
                        self.game.move_map(-myself['new_cordinates'][0], -myself['new_cordinates'][1])
                        self.game.player.cam_x = myself['new_cordinates'][0]
                        self.game.player.cam_y = myself['new_cordinates'][1]
                        self.game.player.initalized = True
                    self.freez_game = False
                
            except (Exception,TimeoutError) as ex:
                self.freez_game = True
                self.send_to_server(self.game.player.data)
                time.sleep(1)
           
    def disconnect(self):
        self.running = False
        self.send_to_server("Disconnected:" + self.game.player.name +":" + self.game.player.roomid)
                
    def connect_to_server(self):
        self.start()

    def send_to_server(self, msg):
        try:
            message = msg
            message = pickle.dumps(message)
            self.UDPClientSocket.sendto(message, self.serverAddress)
        except Exception as e:
            print(f"Error during serialization: {e}")

    def recive_from_server(self):
        try:
            respond, address = self.UDPClientSocket.recvfrom(Client.BYTES_LEN)
            # Deserijalizacija sa pickle
            data = pickle.loads(respond)  # Ovdje dolazi deserijalizacija binarnih podataka
            return {'data':data, 'address':address}
        except Exception as e:
            print(f"Error during deserialization: {e}")

