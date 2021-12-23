from time import sleep
import socket


class client():
    def __init__(self, mode = 0):
        """
        PARAM mode : int , what is the mode of the connnection
        """
        self.mode = mode
        self.game_over = False
        self.udp_socket = None
        self.tcp_socket = None

    def start(self):
        print() 