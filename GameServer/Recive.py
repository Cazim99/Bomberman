import pickle
import threading
import uuid
import time

class Recive(threading.Thread):
    
    BYTES_LEN_RECIVING = 3072
    
    def __init__(self, root):
        super().__init__(target='run', daemon=True)
        self.root = root
        self.queue = root.Queue
        self.clients = root.clients
        self.users = root.users


    def background_task(self, roomid, id):
        print("Bomb activated")
        time.sleep(0.1)
        c = 0
        for n in range(0,10):
            self.root.rooms[roomid]['bombs'][id][2] = c
            if c == 1:
                c = 0
            else:
                c = 1
            time.sleep(0.3)

        self.root.rooms[roomid]['bombs'][id][2] = 1
        print("Bomb exploded")
        time.sleep(0.5)
        self.root.rooms[roomid]['bombs'].pop(id)

    def activate_bomb(self, roomid, id):
        thread = threading.Thread(target=self.background_task,args=(roomid,id),daemon=True)
        thread.start()    
        
    def run(self):
        while True:
      
                user, address = self.recive_from_client()
                
                if "CONNECTED" in user:
                    username = user.split(":")[1]
                    if str(username).strip() in self.users:
                        self.root.send_to_client({'connected':True}, address)
                        continue
                    else:
                        self.root.send_to_client({'connected':False}, address)
                        continue
                
                if "Disconnected" in user:
                    try:
                        self.root.rooms[user.split(":")[2]]['clients'].pop(user.split(":")[1])
                    except Exception as ex:
                        continue
                    continue
                
                if user['username'] in self.users:
                    user['roomid'] = self.users[user['username']]['roomid']
                    if user['initalized'] == True:                            
                        if 'bomb' in user:
                            id = str(uuid.uuid4())
                            self.root.rooms[user['roomid']]['bombs'][id] = [user['bomb'],user['username'], 0]
                            self.activate_bomb(user['roomid'],id)
                            
                        self.queue.put((user, address))
                    else:
                        self.root.rooms[user['roomid']]['users'][user['username']]['new_cordinates'] = self.users[user['username']]['cordinates']
                        self.root.send_to_client({'users':self.root.rooms[new_user['roomid']]}, address)
                        self.root.rooms[user['roomid']]['users'][user['username']].pop('new_cordinates')
                else:
                    # INITALIZE USER
                    new_user = {}
                    new_user['username'] = user['username']
                    new_user['cordinates'] = user['cordinates']
                    new_user['width'] = user['width'] 
                    new_user['height'] = user['height']
                
                    self.users[new_user['username']] = new_user
                    if len(self.root.rooms) == 0:
                        new_user['roomid'] = str(uuid.uuid4())
                        new_user['new_cordinates'] = (-550,-530)
                        self.root.rooms[new_user['roomid']] = {'users':{new_user['username']:new_user},'clients':{new_user['username']:address},'map':self.root.map, 'bombs':{}} 
                    else:
                        for room in self.root.rooms:
                            if len(self.root.rooms[room]['users']) < 2:
                                new_user['roomid'] = room
                                new_user['new_cordinates'] = (550,530)
                                self.root.rooms[room]['users'][new_user['username']] = new_user
                                self.root.rooms[room]['clients'][new_user['username']] = address
                                if len(self.root.rooms[room]['users']) == 2: # ako se popuni soba napravi novu
                                    self.root.rooms[str(uuid.uuid4())] = {'users':{}}
                                break
                    
                    self.root.send_to_client({'users':self.root.rooms[new_user['roomid']]}, address)
                    self.root.rooms[new_user['roomid']]['users'][new_user['username']].pop('new_cordinates')
                    print(f"User {new_user['username']} connected !")
                    self.root.output.append(f"User {new_user['username']} connected !")

    
    def recive_from_client(self):
        data, address = self.root.UDPServerSocket.recvfrom(Recive.BYTES_LEN_RECIVING)
        data = pickle.loads(data)
        return [data, address]