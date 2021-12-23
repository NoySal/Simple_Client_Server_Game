from time import sleep
import socket
from client import Client
from threading import Thread

class H_server:
    def __init__(self):
        return

    def start(self):
        print('SERVER : starting demo server')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        message = 'fuck me beautiful'
        while True:
            try:
                print('SERVER : trying to send a message')
                sock.sendto(message.encode() , ("127.0.0.1" , 13117))
            except:
                pass
            sleep(1)
        sock.close()
    
if __name__ == "__main__":
    #def t_func():
    cl = Client(mode=0)
    #cl.start()
    t = Thread(target = cl.start)
    t_srv =H_server()
    t.start()
    t_srv.start()


    #t.join()


