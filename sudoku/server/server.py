import pickle
import socket
import threading
from time import sleep

from sudoku.common.protocol import GAME_UPDATE_PORT
from sudoku.server.player import Player
from sudoku.common import protocol
from sudoku.common.protocol import HOST, PORT
from sudoku.common.session import Session

client_addr_sockets = []

recv_buffer_length = 1024
current_players = []


class GamesHandler:
    """
    A wrapper for the games list and its handling
    """
    current_sessions = []

    def __init__(self):
        self.current_sessions = []
        self.__lock = threading.Lock()

    def __is_name_valid(self, game_name):
        for s in self.current_sessions:
            if s.game_name == game_name:
                return False
        return True

    def new_session(self, information, current_player):
        game_name = information.split(protocol._MSG_FIELD_SEP)[1]

        # if not self.__is_name_valid(game_name):
        #     return None # TODO: be more informative on reasons to client

        max_num_of_players = information.split(protocol._MSG_FIELD_SEP)[2]
        # if max_num_of_players < 1 or max_num_of_players > 100:
        #     return None # TODO: be more informative to client

        s_id = len(self.current_sessions ) + 1
        current_player.current_session_id = s_id
        session = Session('running', s_id, game_name,
                          'sudoku/puzzles/sudoku_easy_1.csv',
                          'sudoku/puzzles/sudoku_easy_1_solution.csv',
                          max_num_of_players,
                          [current_player])
        session.game_start()

        self.__lock.acquire()
        self.current_sessions.append(session)
        self.__lock.release()
        return session

    def join_session(self, information, player):
        try: # if input of int() is not convertible to integer it throws an error
            req_ses_id = int(information.split(protocol._MSG_FIELD_SEP)[1])
        except ValueError:
            print("session id is not int convertible: %s" % information.split(protocol._MSG_FIELD_SEP))
            return # TODO: appropriate error to user

        for session in self.current_sessions:
            if session.game_id == req_ses_id:
                break
        self.__lock.acquire()
        player.current_session_id = session.game_id
        joined_session = session.add_player(player)
        # TODO: some mysterious behavior observed here. couldn't reproduce it [Novin]
        print("player added to current session!")
        self.__lock.release()
        if joined_session:
            return session
        else:
            return None

    def get_session(self, id):
        target_session = None
        for s in self.current_sessions:
            if s.game_id == id:
                target_session = s
        return target_session
        # return self.current_sessions[id]

    def get_sessions(self):
        return self.current_sessions

    def leave_session(self):
        pass

    def get_num_of_sessions(self):
        return len(self.current_sessions)


def client_thread(sock, addr, games):
    print 'created new thread for client', addr

    player = None
    # TODO: maybe it's better to use a hash of clients IP:PORT for that!!
    while True:
        sleep(1)
        try:
            header = sock.recv(recv_buffer_length)
            if protocol.server_process(header) == protocol._SA_NEW_PLAYER:
                player = Player(addr)
                # players.add_player(id = hash(threading.current_thread()))
                current_players.append(player)
                sock.send(protocol._ACK)

            elif protocol.server_process(header) == protocol._SA_NICKNAME:
                player.nickname = header.split(protocol._MSG_FIELD_SEP)[1]
                sock.send(protocol._ACK)

            elif protocol.server_process(header) == protocol._SA_CREATE_SESSION:
                # information = client_socket.recv(recv_buffer_length)
                created_session = games.new_session(header, player)
                pickle_session = pickle.dumps(created_session)
                sock.send(pickle_session)

            elif protocol.server_process(header) == protocol._SA_JOIN_SESSION:
                joined_session = games.join_session(header, player)
                if joined_session:
                    pickle_session = pickle.dumps(joined_session)
                    sock.send(pickle_session)
                else:
                    sock.send(protocol._RSP_SESSION_FULL)

            elif protocol.server_process(header) == protocol._SA_CURRENT_SESSIONS:
                pickle_current_sessions = pickle.dumps(games.get_sessions())
                sock.send(pickle_current_sessions)

            elif protocol.server_process(header) == protocol._SA_UPDATE_GAME:
                print(header)
                # TODO: update Score - player.updateScore(header_part2)
                # TODO: give in the game_id
                s = player.current_session_id
                my_session = games.get_session(s)

                if my_session:
                    correct = my_session.update_game(header, player)
                else:
                    print("error: no session with id %d found!" % s)
                    continue

                print my_session.game_state

                pickle_session = pickle.dumps((my_session, correct))
                sock.send(pickle_session)
                # send to other players of the same session
                for other_player in my_session.current_players:
                    # TODO: exlude the current player that upated the game!
                    # if other_player != player:
                    other_player.send_game_updates(my_session)
                    print "game updates sent to ", other_player.nickname


            elif header == protocol._TERMINATOR:
                break
        except Exception as e:
            print(e)
            continue
        except KeyboardInterrupt as e:
            break

    # if reached here then connection had to be terminated
    sock.close()
    player.delete()


def handle_link_backs(games):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, GAME_UPDATE_PORT))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.listen(0)
    while True:
        client_sock, client_addr = sock.accept()
        player_id = client_sock.recv(1000)

        found = False
        for sess in games.current_sessions:
            if found:
                break
            for p in sess.current_players:
                if p.nickname == player_id:
                    p.link_back_sock = client_sock
                    found = True
                    print("link back established with player_id: ", player_id)
                    break
        if not found:
            print("no player with id \"%s\" could be matched for link back!" % player_id)
        # TODO: send fail or success


def server_main(args=None):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    backlog = 0
    # server_socket.listen(backlog)

    games = GamesHandler()

    threads = []
    # handle links with thread
    t = threading.Thread(target=handle_link_backs, args=(games,)).start()
    threads.append(t)

    server_socket.listen(backlog)
    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            t = threading.Thread(target=client_thread, args=(client_socket, client_addr, games)).start()
            threads.append(t)
        except KeyboardInterrupt as e:
            break

    # clean-ups
    for thread in threads:
       thread.join()
    server_socket.close()


if __name__ == '__main__':
    server_main()