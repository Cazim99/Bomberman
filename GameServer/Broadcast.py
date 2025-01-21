import threading
import json
import pickle
import uuid

class Broadcast(threading.Thread):
    
    BYTES_LEN_RECIVING = 3072
    
    def __init__(self, root):
        super().__init__(target='run', daemon=True)
        self.root = root
        self.queue = root.Queue
        self.clients = root.clients
        self.users = root.users
    

    def update_user(self, user):
        if user['username'] in self.users:
            self.users[user['username']]['cordinates'] = user['cordinates']
            self.root.rooms[user['roomid']]['users'][user['username']]['cordinates'] = user['cordinates']
    
    def run(self):
        while True:
            while not self.root.Queue.empty():
                try:
                    user, address = self.queue.get()
                    
                    
                    if user is not None and 'username' in user:
                        if user['roomid'] is not None:
                            if user['username'] not in self.root.rooms[user['roomid']]['clients']: # Add user ip addres in clients if dont exists
                                self.root.rooms[user['roomid']]['clients'][user['username']] = address
                            elif self.root.rooms[user['roomid']]['clients'][user['username']] != address: # Check if player maybe changed ip address
                                    self.root.rooms[user['roomid']]['clients'][user['username']] = address
                            
                            self.update_user(user) # Update player new position and other
                            
                            for client in self.root.rooms[user['roomid']]['clients']:
                                self.root.send_to_client({'users':self.root.rooms[user['roomid']]}, self.root.rooms[user['roomid']]['clients'][client])

                except Exception as ex:
                    print(ex)
                    self.root.output.append(ex)