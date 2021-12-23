import socket
from threading import Thread
from time import sleep


Broadcast_PORT = 13117

MyIp = socket.gethostbyname(socket.gethostname())
Con_count=0
Con_lst =[]


def rand_question():
    x='What is 1+1 ?'
    return x

Cur_question = rand_question()


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

def ConnectToPlayer(PlayerSocket , PlayerAdress):


    return
def BroadCast(Thread , PORT):
    try:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udp.bind(("", Broadcast_PORT))

    except:
        print('something went wrong')
