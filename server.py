import socket
from session import Session
from player import Player
import protocol
from time import sleep
import pickle


current_sessions = []
current_players = []


HOST = '127.0.0.1'
PORT = 7777

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




    
                
                
if __name__ == '__main__':
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    backlog = 0
    server_socket.listen(backlog)
    
    while True: 
        #sleep(1)
        try:
            client_socket, client_addr = server_socket.accept()
            while True:
                #sleep(1)
                try:
                    header = client_socket.recv(recv_buffer_length)
                    if protocol.server_process(header) == protocol.__SA_NEW_PLAYER:
                        player1 = Player(client_addr)
                        current_players.append(player1)
                        client_socket.send(protocol.__ACK)

                    elif protocol.server_process(header) == protocol.__SA_NICKNAME:
                        player1.nickname = header.split(protocol.__MSG_FIELD_SEP)[1]
                        client_socket.send(protocol.__ACK)

                    elif protocol.server_process(header) == protocol.__SA_CREATE_SESSION:
                        #information = client_socket.recv(recv_buffer_length)
                        new_session(header)
                        pickle_session = pickle.dumps(current_sessions[0])
                        client_socket.send(pickle_session)
                        #current_sessions.append(new_session)
                        
                    elif protocol.server_process(header) == protocol.__SA_CURRENT_SESSIONS:
                        pickle_current_sessions = pickle.dumps(current_sessions)
                        client_socket.send(pickle_current_sessions)
                        
                    elif protocol.server_process(header) == protocol.__SA_UPDATE_GAME:
                        current_sessions[0].update_game(header)
                        pickle_session = pickle.dumps(current_sessions[0])
                        client_socket.send(pickle_session)
                        

                    elif header == protocol.__TERMINATOR:
                        break
                        
                except KeyboardInterrupt as e:
                    break

        except KeyboardInterrupt as e:
            break
        
        
    server_socket.close()

    
    
    