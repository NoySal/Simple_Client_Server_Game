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

    def connect(self, ip, port):
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.settimeout(30)
            tcp_socket.connect(ip, port)
        except:
            print("failed to connect to server")
        finally:
            self.game(tcp_socket)

    def game(self, tcp_socket):
        try:
            #send team name
            tcp_socket.send('name \n'.encode())

            #recieve math problem
            math_problem = tcp_socket.recv(1024).decode()

            #ask for answer form user and send it to the server
            val = input(math_problem)
            tcp_socket.send(val.encode())

            #recieve game result
            game_result = tcp_socket.recv(1024).decode()
            print(game_result)
        except socket.timeout:
            print("Connection timeout")
        except:
            print("Error occured")

        #disconnect
        tcp_socket.close()
        print("Server disconnected, listening for offer")

        #quit game
        self.game_over = True

    def send(self, messege):
        while self.udp_socket==None:
            #try to create a udp socket
            print('DEBUG - udp socket loop entered')
            self.udp_socket = self.assign_socket()

            #wait a bit
            sleep(0.5)

    def start(self):
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
        def parse(msg):
            """
            function to parse UDP messages according to requested structure.
            PARAM msg : str , incoming message to parse for specific structure
            returns port if structure is according to expectations
            """
            try:
                if int(msg[:10]) != 2882395322:
                    print('Parsing error - Cookie is wrong!')
                if int(msg[10:11]) != 2:
                    print('Parsing error - option not supported')
                if int(msg[11:]) <= 1024 : 
                    print('Port is suspicious - system port detected')              
            except:
                print('parsing exception - message too short , length !' , len(msg))
                return

            return int(msg[12:])

        udp_error =0
        while True:
            print('DEBUG - listening loop&parsing entered')
            try:
                message,serverAddress = self.udp_socket.recvfrom(2048)
                print('message decoded is ' , message.decode())
                port = parse(message)

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