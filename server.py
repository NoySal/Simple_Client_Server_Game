from contextlib import nullcontext
import socket
from threading import Thread, Lock
from time import sleep


class Server:
    def __init__(self, mode = 0):
        """
        PARAM mode : int , what is the mode of the connnection
        """
        self.mode = mode
        self.teams_arr_lock = Lock()
        self.winner_lock = Lock()
        self.tcp_socket = None
        self.ip = self.get_ip()
        self.question = self.rand_question()
        self.teams = []
        self.game_ready = False
        self.winner = None

    def Start(self):
                  
                  
        print(f'Server started, listening on {self.ip}')

        while self.tcp_socket == None:

            tcp_port = self.tcp_port_create()

        broadcast_thread = Thread(self.send_udp_broadcast , args = (tcp_port)) 
        broadcast_thread.start()
        ConnectionHandler = Thread(self.TCP_listner )
        ConnectionHandler.start()

        while True:

            while not self.game_ready:    #  waiting for 2 players
                self.teams_arr_lock.acquire()

                try:

                    if len(self.teams) ==2:

                        self.game_ready = True
                finally:
                    self.teams_arr_lock.release()


            while self.winner ==None: #game is running
                sleep(5)

            self.create_stats()

            ##recycle variables
            self.question = self.rand_question()
            self.teams = []
            self.game_ready = False
            self.winner = None

            print('Game over, sending out offer requests...')     
  
    def create_stats(self):
        """
        TODO :  Something cute to keep games statistics.
        """   

    def rand_question(self):
        """
        TODO : this func to randomize questions and answers
        """
        return ('2 + 2', '4')


    def ConnectionHandler(self):
        """
        Thread method for listening to a TCP port , and creating new threads for incoming connections.
        """
        print('DEBUG - Connection handler is live')
        try:
            self.tcp_socket.listen(2)   #wait for 2 incoming connections
            while True:
                client_sock , client_add = self.tcp_socket.accept()
                print(f'DEBUG - connection accepted from {client_add}')
                player_thread = Thread(self.ManageTeam , args = (client_sock , client_add))
                player_thread.start()

                #I'm not sure about sleeping here , but fuck it.
                sleep(0.2) 

        except:
            print('EXCEPT connection handler encountered an error and will quit!')
        

    def send_udp_broadcast(self , port): 
        """
        Broadcaster threaded function. acquires UDP port and broadcast offers every 1 sec
        PARAM port: int ,  TCP port the server listening on 
        """

        while True:  #outer loop UDP acquisition failures for failures

            try:
                server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                server_udp.bind((self.ip, 13117))

            except:
                print('Error while getting socket')
                server_udp.close()
                #port initialization failed - wait a bit and try again
                sleep(2)
                continue

            print('Server started, listening in IP address ' + self.ip)

            try:
                while not self.game_ready:   #broadcast if there is no game happening
                    msg = str(0xabcddcba) + str(0x2) + str(port)
                    server_udp.send(msg.encode())
                    sleep(1)
            except:
                print('Broadcast message failed  , sleeping and trying again')

            #we are in a game session!
            sleep(10)

    def ManageTeam(self, tcp_socket, add):
        """
        Thread method for accepted connection , runs the whole game session.
        PARAM sock : socket of the accepted TCP connection
        param add : ip adress of accepted TCP connection 
        """
        try:
            team_name = tcp_socket.recv(1024).decode()

            self.teams_arr_lock.acquire()
            try:
                self.teams.append(team_name)
            finally:
                self.teams_arr_lock.release()
            
            while not self.game_ready:
                sleep(0.1) #check if other team is ready, low inteval to not give them headstart
            sleep(10)
            #game starts
            welcome_msg = 'Welcome to Quick Maths. \n' \
                          f'Player 1: {self.teams[0]} \n' \
                          f'Player 2: {self.teams[1]} \n' \
                          '== \n' \
                          'Please answer the following question as fast as you can: \n'
            game_msg = welcome_msg + self.question[0]
            tcp_socket.send(game_msg.encode())
            answer = tcp_socket.recv(1024).decode()
            if self.winner_lock.acquire():
                if self.winner == None:
                    if answer == self.question[1]:
                        self.winner = team_name
                    else:
                        self.winner = set(self.teams).difference(set(team_name))[0]
                    self.winner_lock.release()
            else: #other team answered first
                while self.winner == None: #wait until other thread updates winner
                    sleep(0.5)
            game_result = 'Game over! \n' \
                          f'The correct answer was {self.question[1]}! \n' \
                          f'Congratulations to the winner: {self.winner}'
            tcp_socket.send(game_result.encode())
        except socket.timeout: #time out - draw
            print('no team answered in 10 seconds, draw')
        except:
            print('Error during game')
                
    def get_ip(self):
        """
        returns the IP according to environment. local\ dev \ test
        TODO: This method needs to be changed according to test \ dev zones
        
        """
        if self.mode==0:
            return ""

    def tcp_port_create(self):
        """
        Creates a new TCP port on required IP , and returns the tcp port assigned.
        retuns : tcp port.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(self.ip , 0)
        except socket.error:
            print('Failed to create and initialize socket')
            return False

        self.tcp_socket = sock
        return sock.getsockname()[1]   #return assigned port
    
        
