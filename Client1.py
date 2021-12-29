from time import sleep
import socket
from client import Client
from threading import Thread
from server import Server
import scapy

cl = Client('Halva' ,mode=1)
t = Thread(target = cl.start)
t.start()
