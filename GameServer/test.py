import socket
import pickle
import threading
import time
import os

class Server(threading.Thread):
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(4) # If reciving data from server take more then 4 secounds try reconnecting 
    BYTES_LEN = 3072
    
    running = True
    freez_game = True
    saveddata = None
    
    def __init__(self, game):
        self.game = game
        self.serverAddress = (game.server[0], game.server[1])
        super().__init__(target="run", daemon=True)
        
    def run(self):
        self.send_to_server(self.game.player.data)
        while self.running:
            try:
                data_from_server = self.recive_from_server()['data']
                
                if 'users' in data_from_server:
                    myself = data_from_server['users'][self.game.user['username']] 
                    self.freez_game = False
                
            except (Exception,TimeoutError) as ex:
                print(ex)
                self.freez_game = True
                self.send_to_server(self.game.player.data)
                time.sleep(1)
                
    def connect_to_server(self):
        self.start()

    def send_to_server(self, msg):
        message = msg
        message = pickle.dumps(message)
        self.UDPClientSocket.sendto(message, self.serverAddress)

    def recive_from_server(self):
        respond = self.UDPClientSocket.recvfrom(Server.BYTES_LEN)
        data = pickle.loads(respond[0])
        address = respond[1]
        return {'data':data, 'address':address}

