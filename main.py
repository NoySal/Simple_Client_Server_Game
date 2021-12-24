from time import sleep
import socket
from client import Client
from threading import Thread
from server import Server
import scapy 
class H_server:
    def __init__(self):
        return

    def start(self):
        print('SERVER : starting demo server')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        message = str(0xabcddcba) + str(0x2) + str(2020)
        while True:
            try:
                print('SERVER : trying to send a message')
                sock.sendto(message.encode() , ("127.0.0.1" , 13117))
            except:
                pass
            sleep(1)
        sock.close()
    
if __name__ == "__main__":

    cl = Client('Halva' ,mode=0)
    cl2 = Client('Bamba' ,mode=0)


    t = Thread(target = cl.start)
    
    t_srv =Server()

    t.start()

    t2 = Thread(target = cl2.start)
    t2.start()
    t_srv.Start()
    



    #t.join()


