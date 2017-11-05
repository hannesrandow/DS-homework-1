import socket
from server_session import ServerSession
import protocol


current_sessions = []
current_players = []

HOST = '127.0.0.1'
PORT = 7777

recv_buffer_length = 1024


def new_session(information):
    
    game_name = information.split(protocol.__MSG_FIELD_SEP)[0]
    max_num_of_players = information.split(protocol.__MSG_FIELD_SEP)[1][0]
    server_session = ServerSession('running', 1, game_name, 
                                   'sudoku_puzzles/sudoku_easy_1.csv', 
                                   'sudoku_puzzles/sudoku_easy_1_solution.csv', 
                                   max_num_of_players)
    server_session.game_start()
    
    for i in server_session.game_state:
        print i

    
    
def list_sessions():
    return current_sessions

    
                
                
if __name__ == '__main__':
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    backlog = 0
    server_socket.listen(backlog)
    
    while True: 
        
        try:
            client_socket, client_addr = server_socket.accept()
            header = client_socket.recv(recv_buffer_length)
            if protocol.server_process(header) == protocol.__SA_CREATE_SESSION:
                client_socket.send(protocol.__ACK)
                information = client_socket.recv(recv_buffer_length)
                new_session(information)

            else:
                print 'error'

        except KeyboardInterrupt as e:
            break
        
        
    server_socket.close()

    
    
    