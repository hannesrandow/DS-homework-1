import socket
from session import Session
from player import Player
import protocol
from time import sleep
import pickle
import threading
from SocketServer import ThreadingMixIn


current_sessions = []
current_players = []
client_addr_sockets = []


HOST = '127.0.0.1'
PORT = 7789

recv_buffer_length = 1024


def new_session(information):
    
    game_name = information.split(protocol.__MSG_FIELD_SEP)[1]
    max_num_of_players = information.split(protocol.__MSG_FIELD_SEP)[2]
    session = Session('running', 1, game_name, 
                                   'sudoku_puzzles/sudoku_easy_1.csv', 
                                   'sudoku_puzzles/sudoku_easy_1_solution.csv', 
                                   max_num_of_players,
                                   current_players)

    
    session.game_start()    
    current_sessions.append(session)

    
    
def list_sessions():
    return current_sessions



def client_thread(sock, addr):
    while True:
        try:
            header = sock.recv(recv_buffer_length)
            if protocol.server_process(header) == protocol.__SA_NEW_PLAYER:
                player = Player(addr)
                current_players.append(player)
                sock.send(protocol.__ACK)

            elif protocol.server_process(header) == protocol.__SA_NICKNAME:
                player.nickname = header.split(protocol.__MSG_FIELD_SEP)[1]
                sock.send(protocol.__ACK)

            elif protocol.server_process(header) == protocol.__SA_CREATE_SESSION:
                #information = client_socket.recv(recv_buffer_length)
                new_session(header)
                pickle_session = pickle.dumps(current_sessions[0])
                sock.send(pickle_session)
                #current_sessions.append(new_session)
                        
            elif protocol.server_process(header) == protocol.__SA_CURRENT_SESSIONS:
                pickle_current_sessions = pickle.dumps(current_sessions)
                sock.send(pickle_current_sessions)
                    
            elif protocol.server_process(header) == protocol.__SA_UPDATE_GAME:
                current_sessions[0].update_game(header)
                pickle_session = pickle.dumps(current_sessions[0])
                sock.send(pickle_session)
                
            elif header == protocol.__TERMINATOR:
                break
                        
        except KeyboardInterrupt as e:
            break
    
                
                
if __name__ == '__main__':
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    backlog = 0
    #server_socket.listen(backlog)
    
    threads = []
    
    while True: 
        server_socket.listen(backlog)
        try:
            client_socket, client_addr = server_socket.accept()
            client_addr_sockets.append((client_addr, client_socket))
            client_thread = threading.Thread(target=client_thread, args=(client_socket, client_addr))
            client_thread.start()
            threads.append(client_thread)
        except KeyboardInterrupt as e:
            break
        
        
    for thread in threads:
        thread.join()
    server_socket.close()

    
    
    