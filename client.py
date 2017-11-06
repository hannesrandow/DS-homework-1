from socket import AF_INET, SOCK_STREAM, socket
from os import getpid
import protocol
from time import sleep
import pickle

HOST = '127.0.0.1'
PORT = 7777

def get_current_sessions():
    pass

def join_session():
    pass


def create_session():
    pass


def leave_session():
    pass



def send_request(socket, m):
    socket.sendall(m)
    rsp = socket.recv(10000)
    if rsp == protocol.__ACK:
        return True
    else:
        return pickle.loads(rsp)


def process_response(m):
    pass

def create_session(game_name, max_num_players):
    new_session = send_request(socket, 
                                       protocol.__REQ_CREATE_SESSION + protocol.__MSG_FIELD_SEP + 
                                       game_name + protocol.__MSG_FIELD_SEP + max_num_players)
    
    return new_session
    

def nickname(n):
    send_request(socket, protocol.__REQ_NICKNAME + protocol.__MSG_FIELD_SEP + n)
    return 

def connect():
    send_request(socket, protocol.__REQ_INITIAL_CONNECT)
    return



if __name__ == '__main__':
    
    socket = socket(AF_INET, SOCK_STREAM)
    socket.connect((HOST, PORT))
    try:
        #initial_connect = send_request(socket, protocol.__REQ_INITIAL_CONNECT)
        connect()
        #requested_nickname = send_request(socket, protocol.__REQ_NICKNAME + protocol.__MSG_FIELD_SEP + 'first_user')
        nickname('user1')
        current_session = create_session('test_game', '5')

        for i in current_session.game_state:
            print i
        #if socket.recv(1024) == protocol.__ACK:
        #    socket.sendall(protocol.__REQ_UPDATE_GAME + protocol.__MSG_FIELD_SEP + '15-9' + protocol.__TERMINATOR)
    except Exception as e:
        print(e)
    
    