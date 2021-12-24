from time import sleep
import socket


class Client:

    def __init__(self, TeamName,mode = 0):
        """
        PARAM TeamName :  string , what is the name of the Team.
        PARAM mode : int , what is the mode of the connnection
        """
        self.mode = mode
        self.game_over = False
        self.udp_socket = None
        self.tcp_socket = None
        self.ip = self.get_ip()
        self.teamName = TeamName

    def start(self):
        """
        Client start function.
        Forever loop until acquiring socket , then forever loop listening and repeating games.
        """
        while self.udp_socket==None:    

            #try to create a udp socket
            print('DEBUG - udp socket loop entered')
            self.udp_socket = self.assign_socket()

            #wait a bit - rerun if socket acquisition failed
            sleep(0.5)     

        while not self.game_over:

            print('DEBUG - not game over loop entered')
            #fetch messages , get port , try to connect

            servip , servport = self.listen_and_parse()
            print(f'Received offer from {servip}, attempting to connect...')
            
            self.connect(servip , servport)

            self.game()

            #waiting a bit
            sleep(0.5)

    
    def connect(self, ip, port):
        """
        Trying to initiate a TCP connection with parsed ip and port from broadcast
        PARAM ip : string - ip recieved from UDP datagram.
        PARAM port: string  - port parsed from udp message.
        """
        print('DEBUG - trying to connect ')
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.settimeout(30)
            self.tcp_socket.connect(ip, port)
        except:
            self.tcp_socket.close()
            print("failed to connect to server")
            return # connection failed
        

    def game(self):

        print('DEBUG - STARTING A GAME: CLIENT SIDE ')
        try:
            #send team name
            self.tcp_socket.send(str(self.TeamName) + ' \n'.encode())

            #recieve math problem
            math_problem = self.tcp_socket.recv(1024).decode()

            #ask for answer form user and send it to the server
            val = input(math_problem)
            self.tcp_socket.send(val.encode())

            #recieve game result
            game_result = self.tcp_socket.recv(1024).decode()
            print(game_result)

        except socket.timeout:
            print("Connection timeout")
        except:
            print("Error occured")

        #disconnect
        self.tcp_socket.close()
        print("Server disconnected, listening for offer")

        #quit game
        #self.game_over = True
        return 

    def listen_and_parse(self):
        """
        listening to udp port , parsing each message and if its a valid offer - returning ip and port
        returns :  Ip , port of Game Server.
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
            port = None
            try:
                message,serverAddress = self.udp_socket.recvfrom(2048)
                print('message decoded is ' , message.decode())
                port = parse(message)

            except:
                print('udp listening error encoutered')
                udp_error+=1
            if port != None:
                break

            if udp_error==3:
                ##reoccuring error - maybe socket failed , try to reset it
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

        return serverAddress,port

    def assign_socket(self):
        """
        assign yourself with a working udp socket to a desired ip adress
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            sock.bind((self.ip , 13117))
        except:
            sock.close()
            print('UDP socket creating ERROR')
            return None

        print('Client started, listening for offer requests...')
        return sock

    def get_ip(self):
        """
        returns the IP according to environment. local\ dev \ test
        TODO: This method needs to be changed according to test \ dev zones
        
        """
        if self.mode==0:
            return ""