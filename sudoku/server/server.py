"""
The server script
"""

import pickle
import socket
import threading
from time import sleep

import struct

from sudoku.common.protocol import GAME_UPDATE_PORT
from sudoku.server.player import Player
from sudoku.common import protocol
from sudoku.common.protocol import HOST, PORT
from sudoku.common.session import Session
from sudoku.server.ic_server_update import ICServerUpdate

client_addr_sockets = []

recv_buffer_length = 1024
current_players = []    # just for having a list of active players on server (no particular use!)
shouldRunning = True    # a global variable for threads to know when to finish their loop

class GamesHandler:
    """
    A wrapper for the games list and its handling
    """
    current_sessions = []

    def __init__(self, args):
        """
        :param args: Contains the name of the sudoku puzzle
        """
        self.current_sessions = []
        self.__lock = threading.Lock()
        self.sudoku_name = args.filename
        self.sudoku_sol = args.filename + '_solution'

    def __is_name_valid(self, game_name):
        for s in self.current_sessions:
            if s.game_name == game_name:
                return False
        return True

    def new_session(self, information, current_player):
        """
        This method is called when a user creates a new session.
        :param information: Contains the name that the user gave to the game.
        :param current_player: The player that created the session.
        :return: The newly created session.
        """
        game_name = information.split(protocol._MSG_FIELD_SEP)[1]

        # if not self.__is_name_valid(game_name):
        #     return None # TODO: be more informative on reasons to client

        max_num_of_players = information.split(protocol._MSG_FIELD_SEP)[2]
        # if max_num_of_players < 1 or max_num_of_players > 100:
        #     return None # TODO: be more informative to client

        s_id = len(self.current_sessions ) + 1
        current_player.current_session_id = s_id
        session = Session(protocol._PENDING, s_id, game_name,
                          self.sudoku_name,
                          self.sudoku_sol,
        #                  'sudoku/puzzles/sudoku_easy_1.csv',
        #                  'sudoku/puzzles/sudoku_easy_1_solution.csv',
                          max_num_of_players,
                          [current_player])
        session.game_start()

        self.__lock.acquire()
        self.current_sessions.append(session)
        self.__lock.release()
        return session

    def join_session(self, information, player):
        """
        This method gets called when a user reqeusts to join an already up and running session.
        :param information: Contains the id of the session that the user wants to join.
        :param player: The player instance representing the user that wants to join the session
        :return: The session that was joined, if the maximum number of players was not reached yet. None otherwise.
        """
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
        """
        This method gets called when a user requests to get the sessions that are currently running.
        :param id:
        :return:
        """
        target_session = None
        for s in self.current_sessions:
            if s.game_id == id:
                target_session = s
        return target_session
        # return self.current_sessions[id]

    def get_sessions(self):
        """
        This method gets called when a user requests to get the sessions that are currently running.
        :return: A list of the sessions currently running.
        """
        return self.current_sessions

    def leave_session(self):
        pass

    def get_num_of_sessions(self):
        """
        This method gets called when a user requests to get the sessions that are currently running.
        :return: Number of sessions currently running.
        """
        return len(self.current_sessions)


def client_thread(sock, addr, games):
    """
    Handles the all the requests a client makes to the server.
    :param sock: Client socket.
    :param addr: Client address.
    :param games: A gameshandler.
    :return: None
    """
    print 'created new thread for client', addr

    global shouldRunning
    player = None
    # TODO: maybe it's better to use a hash of clients IP:PORT for that!!
    while shouldRunning:
        sleep(1)
        try:
            header = sock.recv(recv_buffer_length)
            if header == '':
                break
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

                for other_player in joined_session.current_players:
                    # TODO: exlude the current player that upated the game!
                    # if other_player != player:
                    other_player.send_game_updates(joined_session)
                    print "[based a join rqst] game updates sent to : ", other_player.nickname

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
                    if other_player != player:
                        other_player.send_game_updates(my_session)
                        print "[based a game update rqst] game updates sent to ", other_player.nickname


            elif header == protocol._TERMINATOR:
                break
        except KeyboardInterrupt as e:
            break
        except Exception as e:
            print("Exception for client", addr)
            print(e)
            print("continue processing..")
            continue

    # if reached here then connection had to be terminated
    print("closing session for client", player.client_ip)
    sock.close()
    print("socket closed")
    player.close()
    print("client link back closed")

    # update list of players
    if player and player.current_session_id:
        current_game = games.get_session(player.current_session_id)
        current_game.current_players.remove(player)  # remove player from his session
        # check on the status of the game if only one player is left -> game completed
        if len(current_game.current_players) == 1:
            current_game.game_status = protocol._COMPLETED
            for other_player in current_game.current_players:
                other_player.send_game_updates(current_game)
                print "only one player left -> game ends for : ", other_player.nickname

        current_players.remove(player)  # remove player from current_players list
        print("current_players list being updated..")
        player = None
    else:
        print("player object is none [weird!!]")




def handle_link_backs(games):
    """
    Becomes redundant through publish/subscribe pattern
    This method takes care of the link backs, which are used to send the session to the client.
    :param games: A gameshandler
    :return: None
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, GAME_UPDATE_PORT))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_KEEPALIVE, 1)

    sock.listen(0)
    while shouldRunning:
        client_sock, client_addr = sock.accept()
        player_id = client_sock.recv(1000)
        id = pickle.loads(player_id)

        found = False
        for sess in games.current_sessions:
            if found:
                break
            for p in sess.current_players:
                if p.client_ip == id:
                    p.link_back_sock = client_sock
                    found = True
                    print("link back established with player_id: ", player_id)
                    break
        if not found:
            print("no player with id \"%s\" could be matched for link back!" % player_id)
        # TODO: send fail or success
    print("link back checker on threading side got dismissed!!!")


def game_server_beacon(interval):
    """sending packets for discovery of this game server"""
    print("start game server discovery packets..")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    # ttl = struct.pack('b', 1)
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    while shouldRunning:
        sleep(interval)
        sock.sendto(protocol.service_name, protocol.multicast_group)
        # TODO: do LOG.debug
        print('[discovery] beep..')
        # print('send discovery packets to multicast group [%s]' % protocol.multicast_group[0])


def server_main(args=None):
    """
    Main thread to run the server
    :param args: Arguments passed to server. Game
    :return: None
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    backlog = 0
    # server_socket.listen(backlog)

    games = GamesHandler(args)
    global shouldRunning
    threads = []
    # handle links with thread
    t = threading.Thread(target=handle_link_backs, args=(games,)).start()
    threads.append(t)

    # game server discovery beacon
    interval = 2   # 2 secs discovery_signal_interval
    t = threading.Thread(target=game_server_beacon, args=(interval,)).start()
    threads.append(t)

    server_socket.listen(backlog)
    while True:  # grand loop of the server
        try:
            client_socket, client_addr = server_socket.accept()
            t = threading.Thread(target=client_thread, args=(client_socket, client_addr, games)).start()
            threads.append(t)
        except KeyboardInterrupt as e:
            shouldRunning = False
            break

    # clean-ups
    for thread in threads:
       thread.join() # FIXME: cannot join game server discovery thread.. why?
    server_socket.close()


if __name__ == '__main__':
    server_main()