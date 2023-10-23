from lcu_driver import Connector
import asyncio
import threading
import time
import json
import requests
import urllib3
import catInstance as Cat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


headers = {'accept': 'application/json',
           'Authorization': 'Basic cmlvdDo3Z0FKeWZreDZQYi1iNlZpMkM1d1R3',
           'content-Type': 'application/json'
           }

connector = Connector()

dataQueue = []

baseCommands = ['feed', 'pet']

# Listener
# Fills dataQueue with intercepted user messages

def webSocket():
    @connector.ready
    async def connect(connection):
        print("ready")

    @connector.ws.register('/lol-chat/v1/conversations/', event_types=('CREATE',))
    async def chat_update(connection, event):
        if event.data['type'] == 'chat':
            dataQueue.append((event.data['fromId'], event.data['body']))

    connector.start()


def catUpdateFace(cat):
    ip = 'https://127.0.0.1:60802/lol-chat/v1/me'
    packet = {"statusMessage": str(cat)}
    print('entry', packet['statusMessage'])
    data = json.dumps(packet, ensure_ascii=False).encode('utf-8')
    r = requests.put(ip, verify=False, headers=headers, data=data)
    
    if r.status_code != 201:
        print("Failed", r.json())
    else:
        #print(r.json()["statusMessage"])
        print("good, 201")


def catResponse(cat):
    # Todo: implement message response using sql


    packet = {
        'body': '',
        'fromId': '81ae2f4e-7620-5e4f-b6d1-28c3835bc6fa@na1.pvp.net',
        'type': 'chat'
        }


    if len(dataQueue) == 0:
        return
    msg = dataQueue.pop(0)

    if msg[1][:4] != '/cat':
        return

    command = msg[1][4:].lower().split()

    #help
    if len(command) == 0 or command[0] not in baseCommands:
        packet['body'] = 'You can interact with the cat using /cat feed [food] or /cat pet. Meow!'
        
    # feed case
    elif command[0] == baseCommands[0]:
        if len(command) < 2:
            # too short
            packet['body'] = 'You gave out your hand to feed the cat, but your hand was empty! Kitty is not pleased. Usage: /cat feed [food]'
            cat.happiness = max(cat.happiness - 1, 0)
        else:
            #assess value of command[1] and change cat happiness
            cat.happiness = min(cat.happiness + 5, 10)
            packet['body'] = 'You fed the cat some [' + command[1] + ']! Kitty seems to be pleased'

    elif command[0] == baseCommands[1]:
        cat.happiness = max(cat.happiness + 1, 10)
        packet['body'] = 'You pet the cat. Meow!~~ It seems to enjoy the company.' 


    data = json.dumps(packet, ensure_ascii=False).encode('utf-8')
    ip = 'https://127.0.0.1:60802/lol-chat/v1/conversations/' 
    r = requests.post(ip+msg[0]+'/messages', verify=False, headers=headers, data=data)
    if r.status_code != 201:
        print(r.json())
    else:
        print(r.json()["statusMessage"])

    
# Main state loop
def tick():

    # use sql to load in cat
    cat = Cat.Cat("catFaces2.txt")
    

    while 1:
        time.sleep(5)
        
        # Send msg response
        catResponse(cat)

        # Tick cat state
        cat.tick()

        # Update Face
        if cat.needUpdate():
            catUpdateFace(cat) 


# Create start threads
thread1 = threading.Thread(target=webSocket)
thread2 = threading.Thread(target=tick)
thread1.start()
thread2.start()

