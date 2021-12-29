from client import Client
from threading import Thread
from server import Server
import scapy.all as scapy
from time import sleep
import struct
import random
def Only_client(mode = 0):
    cl = Client('Halva' ,mode=mode)
    t = Thread(target = cl.start)
    t.start()
    t.join()

def Client_Server(mode = 0):
    cl = Client('Bamba' ,mode=mode)
    t = Thread(target = cl.start)
    t.start()
    serv = Server(mode = mode)
    serv.Start()


def Only_Server(mode =0):
    ser=Server(mode =mode)
    ser.Start()


if __name__=="__main__":

    #Client_Server(mode = 1)
    #sleep(1)
    #Only_client(1)
    #add = scapy.get_if_addr("eth1")
    #print(type(add))

    #Only_Server(1)
    #packed= struct.pack('IBH' , 0xabcddcba , 0x2 , 545)
    #packed2= struct.pack('dbh' , 0xabcddcba , 0x2 , 545)
    #print(struct.unpack('IBH' ,packed ))

    print(random.sample(['1' , '2'] ,1 )[0])
    #print(packed2)
