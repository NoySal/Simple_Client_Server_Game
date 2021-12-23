import socket
from threading import Thread, Lock
from time import sleep
#change
class Server:
    def __init__(self, mode = 0):
        """
        PARAM mode : int , what is the mode of the connnection
        """
        self.mode = mode
        self.teams = []
        self.game_ready = False
        self.winner = None
        self.winner_lock = Lock()
        self.question = ('2 + 2', '4')

    def main(self):
        broadcast_thread = Thread(send_udp_broadcast, args= ('udp_port'))
        connection_thread_1 = Thread(ManageTeam, args= ('ip, port'))
        connection_thread_2 = Thread(ManageTeam, args= ('ip, port'))
        # need to add - broadcast kill

        while len(self.teams) != 2:
            sleep(0.5)
        self.game_ready = True #threads start to manage game

    def send_udp_broadcast(self, udp_port): #noy
        #this function broadcasts every 1 second
        try:
            server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            server_udp.bind(("", udp_port))

        except:
            print('Error while getting socket')

        finally:
            try:
                while True: #change this True
                    msg = 'Server started, listening in IP address _____'
                    server_udp.send(msg.encode())
                    sleep(1)
            except:
                print('something went wrong')

    def ManageTeam(self, ip, port):
        #establich tcp connection with the team
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.settimeout(10)
            tcp_socket.connect(ip, port)
        except:
            print("failed to connect to server")
        finally:
            # manage the game
            try:
                team_name = tcp_socket.recv(1024).decode()
                self.teams.append(team_name)
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
                    if answer == self.question[1]:
                        self.winner = team_name
                    else:
                        self.winner = set(self.teams).difference(set(team_name))[0]
                    #release lock? can be a problem..

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








Broadcast_PORT = 13117

MyIp = socket.gethostbyname(socket.gethostname())
Con_count=0
Con_lst =[]

def start():
    try:
        ##setup a tcp socket , and get an open port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        OurPort =sock.getsockname()[1]
        sock.listen(2)
        print('Server started, listening on IP address '+str(MyIp))
        
        while True:
            sleep(0.2)
            cSock, cAdd = sock.accept()

            t_con = Thread(target = self.ConnectToPlayer,args = (cSock, cAdd))
            t_con.start()

    except socket.error:
        print('something went wrong')
    finally:
        sock.close()





