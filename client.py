from socket import AF_INET, SOCK_STREAM, socket
from os import getpid
import protocol

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



def send_request():
    pass


def process_response():
    pass



if __name__ == '__main__':
    
    socket = socket(AF_INET, SOCK_STREAM)
    socket.connect((HOST, PORT))

    
    try:
        # file size
        socket.send(protocol.__REQ_CREATE_SESSION + protocol.__MSG_FIELD_SEP + protocol.__TERMINATOR)
        print "sent"
        rsp = socket.recv(1024)
        print "received"
        if rsp == protocol.__ACK:
            socket.sendall('test_game' + protocol.__MSG_FIELD_SEP + '5' + protocol.__TERMINATOR)
            
        else:
            print "unknown message"
            
    except Exception as e:
        print(e)
    
    