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
    
    game_name = information.split(protocol._MSG_FIELD_SEP)[1]
    max_num_of_players = information.split(protocol._MSG_FIELD_SEP)[2]
    session = Session('running', 1, game_name, 
                                   'sudoku_puzzles/sudoku_easy_1.csv', 
                                   'sudoku_puzzles/sudoku_easy_1_solution.csv', 
                                   max_num_of_players,
                                   current_players)

    
    session.game_start()    
    current_sessions.append(session)
    

def join_session(information):
    
    req_ses_id = int(information.split(protocol._MSG_FIELD_SEP)[1])
    for session in current_sessions:
        if session.game_id == req_ses_id:
            break
    if session.max_num_of_players - len(session.current_players) > 0:
        return (True, session)
    else:
        return (False, '_')

    
    
def list_sessions():
    return current_sessions



def client_thread(sock, addr):
    while True:
        print 'created new thread'
        sleep(1)
        try:
            header = sock.recv(recv_buffer_length)
            if protocol.server_process(header) == protocol._SA_NEW_PLAYER:
                player = Player(addr)
                current_players.append(player)
                sock.send(protocol._ACK)

            elif protocol.server_process(header) == protocol._SA_NICKNAME:
                player.nickname = header.split(protocol._MSG_FIELD_SEP)[1]
                sock.send(protocol._ACK)

            elif protocol.server_process(header) == protocol._SA_CREATE_SESSION:
                #information = client_socket.recv(recv_buffer_length)
                new_session(header)
                pickle_session = pickle.dumps(current_sessions[0])
                sock.send(pickle_session)
            
            elif protocol.server_process(header) == protocol._SA_JOIN_SESSION:
                reqest_session = join_session(header)
                if request_session[0]:
                    request_session[1].current_players.append(player)
                    pickle_session = pickle.dumps(request_session[0])
                    sock.send(pickle_session)
                else:
                    sock.send(protocol._RSP_SESSION_FULL)
                        
            elif protocol.server_process(header) == protocol._SA_CURRENT_SESSIONS:
                pickle_current_sessions = pickle.dumps(current_sessions)
                sock.send(pickle_current_sessions)
                    
            elif protocol.server_process(header) == protocol._SA_UPDATE_GAME:
                # TODO: update Score - player.updateScore(header_part2)
                current_sessions[0].update_game(header)
                pickle_session = pickle.dumps(current_sessions[0])
                sock.send(pickle_session)
                
            elif header == protocol._TERMINATOR:
                break
                        
        except KeyboardInterrupt as e:
            break
    
                
                
if __name__ == '__main__':
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    backlog = 0
    #server_socket.listen(backlog)
    
    threads = []
    server_socket.listen(backlog)
    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            threading.Thread(target=client_thread, args=(client_socket, client_addr)).start()
        except KeyboardInterrupt as e:
            break
        
        
    #for thread in threads:
    #    thread.join()
    server_socket.close()

    
    
    