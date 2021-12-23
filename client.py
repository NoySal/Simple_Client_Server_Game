from time import sleep
import socket


class Client:
    def __init__(self, mode = 0):
        """
        PARAM mode : int , what is the mode of the connnection
        """
        self.mode = mode
        self.game_over = False
        self.udp_socket = None
        self.tcp_socket = None

    def start(self):

        while self.udp_socket==None:
            #try to create a udp socket
            print('DEBUG - udp socket loop entered')
            self.udp_socket = self.assign_socket()

            #wait a bit
            sleep(0.5)

        while not self.game_over:
            print('DEBUG - not game over loop entered')
            #fetch messages
            self.listen_and_parse()

            #try to connect

            try:
                pass
                
            except:
                print('game connect')
            #waiting a bit
            sleep(0.5)

    def listen_and_parse(self):
        """
        listening to udp port
        """
        udp_error =0
        while True:
            print('DEBUG - listening loop&parsing entered')
            try:
                message,serverAddress = self.udp_socket.recvfrom(2048)
                print('message recieved is : ' , message)


            except:
                print('udp listening error encoutered')
                udp_error+=1

            if udp_error==3:
                ##reoccuring error - maybe socket failed
                print('trying to restart socket')
                try:
                    self.udp_socket.close()
                except:
                    print('closing socket failed')
                
                self.udp_socket = self.assign_socket()
                if self.udp_socket!= None:
                    udp_error=0
            #wait a bit
            sleep(0.5)

        return ip,port

    def assign_socket(self):
        """
        assign yourself with a working udp socket to a desired ip adress
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            #which ip are we connecting to ? localhost\test\dev
            if self.mode==0:
                ip =""
            
            sock.bind((ip , 13117))
        except:
            sock.close()
            print('UDP socket creating ERROR')
            return None

        finally:

            print('Client started, listening for offer requests...') 
            
        return sock