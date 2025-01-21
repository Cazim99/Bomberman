import socket
import pickle
from ConfigLoader import ConfigLoader
import threading
import queue
from Recive import Recive
from Broadcast import Broadcast
import pygame
import os

import time


class GameServer(threading.Thread):
    
    def __init__(self):
        super().__init__(target='run')

        config_file_informations = {
            "settings":
                {
                    'items':{
                        'server_host':'str',
                        'server_port':'int',
                    }
                },
        }

        CONFIGURATIONS = ConfigLoader.Load(f"{os.getcwd()}/Bomberman/GameServer/config.ini", config_file_informations) # Load all configurations

        # SERVER CONFIG
        SERVER_CONFIGS = CONFIGURATIONS['settings']['items']


        # UDP
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((SERVER_CONFIGS['server_host'], SERVER_CONFIGS['server_port']))

        self.output = []
        self.clients = {}
        self.users = {}
        self.rooms = {}
        self.Queue = queue.Queue()
        self.map = ['#','#','#','#','#','#','#','#','#','#'
                    ,'#','1','1','0','0','0','0','1','1','#'
                    ,'#','1','0','0','0','0','0','0','1','#'
                    ,'#','0','0','#','0','0','#','0','0','#'
                    ,'#','0','0','0','0','0','0','0','0','#'
                    ,'#','0','0','0','0','0','0','0','0','#'
                    ,'#','0','0','#','0','0','#','0','0','#'
                    ,'#','1','0','0','0','0','0','0','1','#'
                    ,'#','1','1','0','0','0','0','1','1','#'
                    ,'#','#','#','#','#','#','#','#','#','#']
        
        
        self.reciving_data_from_clients = Recive(self).start()
        self.broadcast_data_from_clients = Broadcast(self).start()
    
    def send_to_client(self, msg, client_addres):
        message =  pickle.dumps(msg)
        self.UDPServerSocket.sendto(message, client_addres)

    def run(self):
        while True:
            time.sleep(1)
            if input("") == "exit":
                break

if __name__ == "__main__":
    server = GameServer()
    server.start()
    
            







