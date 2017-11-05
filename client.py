from socket import AF_INET, SOCK_STREAM, socket
from os import getpid
import protocol
from time import sleep
import pickle

HOST = '127.0.0.1'
PORT = 7777

current_session = None

def get_current_sessions():
    pass

def join_session():
    pass


def create_session():
    pass


def leave_session():
    pass



def send_request():
    pass


def process_response():
    pass



if __name__ == '__main__':
    
    socket = socket(AF_INET, SOCK_STREAM)
    socket.connect((HOST, PORT))

    
    try:
        socket.send(protocol.__REQ_INITIAL_CONNECT + protocol.__MSG_FIELD_SEP + protocol.__TERMINATOR)
        if socket.recv(1024) == protocol.__ACK:
            socket.send(protocol.__REQ_NICKNAME + protocol.__MSG_FIELD_SEP + 'first_user' + protocol.__MSG_FIELD_SEP + protocol.__TERMINATOR)
            if socket.recv(1024) == protocol.__ACK:
                socket.sendall(protocol.__REQ_CREATE_SESSION + protocol.__MSG_FIELD_SEP + 'test_game' + protocol.__MSG_FIELD_SEP + '5' + protocol.__TERMINATOR)
                #socket.sendall(protocol.__TERMINATOR)
                session = pickle.loads(socket.recv(10000))
                current_session = session
                for i in current_session.game_state:
                    print i
                #if socket.recv(1024) == protocol.__ACK:
                #    socket.sendall(protocol.__REQ_UPDATE_GAME + protocol.__MSG_FIELD_SEP + '15-9' + protocol.__TERMINATOR)
            
                
                
        else:
            print "unknown message"
    
            
    except Exception as e:
        print(e)
    
    