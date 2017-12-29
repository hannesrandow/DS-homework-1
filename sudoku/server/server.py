"""
The server script
"""

import pickle
import socket
import threading
from time import sleep
import struct
from sudoku.server.player import Player
from sudoku.common import protocol
from sudoku.common.session import Session
from sudoku.server.rpc_server import RpcServer
from sudoku.server.ic_server_update import ICServerUpdate

client_addr_sockets = []

recv_buffer_length = 1024
global current_players
current_players = {}
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
        # list of tuples containing session and corresponding ic_server_update
        self.current_sessions = []
        self.__lock = threading.Lock()
        self.sudoku_name = args.filename
        self.sudoku_sol = args.filename + '_solution'
        self.ic_server_updates = []

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
                          max_num_of_players,
                          [current_player])
        session.game_start()
        # this is the publish/subscribe that is used to send updates to all clients in the game
        ic_server_update = ICServerUpdate(game_name=game_name, session=session)
        self.__lock.acquire()
        self.current_sessions.append((session, ic_server_update))
        self.__lock.release()
        #return session
        return

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

        sessions = [s[0] for s in self.current_sessions]
        for session in sessions:
            if session.game_id == req_ses_id:
                break
        self.__lock.acquire()
        player.current_session_id = session.game_id
        joined_session = session.add_player(player)
        print 'joined session ', joined_session
        print 'players: ', ' '.join([p.nickname for p in session.current_players])
        # TODO: some mysterious behavior observed here. couldn't reproduce it [Novin]
        print("player added to current session!")
        self.__lock.release()
        if joined_session:
            #return session
            return session.game_name
        else:
            return None

    def update_session(self, msg, index, player):
        """
        Client requests to make an update to the current session.
        :param index: Index of the session and the ic_server_update instance in the current_sessions list.
        :return:
        """
        if msg.split(protocol._MSG_FIELD_SEP)[1] != protocol._INIT:
            self.current_sessions[index][0].update_game(msg, player)
        self.current_sessions[index][1].publish_update(self.current_sessions[index][0])
        return

    def get_session(self, id):
        """
        This method gets called when a user requests to get the sessions that are currently running.
        :param id:
        :return:
        """
        target_session = None
        sessions = [s[0] for s in self.current_sessions]
        print 'Sessions ', sessions
        for s in sessions:
            if s.game_id == id:
                target_session = s
        print 'target session ', target_session
        tup_index = sessions.index(target_session)
        print tup_index
        return tup_index
        #return target_session
        # return self.current_sessions[id]

    def get_sessions(self):
        """
        This method gets called when a user requests to get the sessions that are currently running.
        :return: A list of the sessions currently running.
        """
        sessions = [s[0] for s in self.current_sessions]
        return sessions

    def leave_session(self, player):
        index = self.get_session(player.current_session_id)#.remove_player(player)
        # TODO: use link back to inform other users
        self.current_sessions[index][0].remove_player(player)
        self.current_sessions[index][1].publish_update(self.current_sessions[index][0])
        del (current_players[player.uuid])
        return True

    def get_num_of_sessions(self):
        """
        This method gets called when a user requests to get the sessions that are currently running.
        :return: Number of sessions currently running.
        """
        return len(self.current_sessions)


def request_handler(msg, uuid, args):
    print 'handle client %s request', uuid
    games = args[0] # FIXME: do something like we get from thread.Thread.create(args=)
    global current_players

    print msg

    if msg == '':
        return

    if protocol.server_process(msg) == protocol._SA_NEW_PLAYER:
        print("NEW PLAYER RQST")
        current_players[uuid] = Player(uuid)
        return protocol._RSP_OK

    elif protocol.server_process(msg) == protocol._SA_NICKNAME:
        print("NICKNAME RQST")
        if uuid not in current_players.keys():
            return protocol._RSP_USER_NOT_EXISTING

        player = current_players[uuid]
        player.nickname = msg.split(protocol._MSG_FIELD_SEP)[1]
        return protocol._RSP_OK

    elif protocol.server_process(msg) == protocol._SA_CREATE_SESSION:
        print("CREATE SESSION RQST")
        if uuid not in current_players.keys():
            return protocol._RSP_USER_NOT_EXISTING

        player = current_players[uuid]
        games.new_session(msg, player)
        return protocol._ACK
    #testing purposes
    elif msg == 'test':
        games.test()
        return protocol._ACK

    elif protocol.server_process(msg) == protocol._SA_JOIN_SESSION:
        print("JOIN SESSION RQST")
        if uuid not in current_players.keys():
            return protocol._RSP_USER_NOT_EXISTING

        player = current_players[uuid]
        joined_session = games.join_session(msg, player)
        if joined_session:
            rsp = protocol._ACK + protocol._MSG_FIELD_SEP + joined_session
            return rsp
            # TODO: send session through other channel!
        else:
            return protocol._RSP_SESSION_FULL


    elif protocol.server_process(msg) == protocol._SA_CURRENT_SESSIONS:
        print("GET CURRENT SESSIONS RQST")
        return pickle.dumps(games.get_sessions())

    elif protocol.server_process(msg) == protocol._SA_UPDATE_GAME:
        print("GAME UPDATE RQST")
        # TODO: update Score - player.updateScore(header_part2)
        # TODO: give in the game_id
        if uuid not in current_players.keys():
            return protocol._RSP_USER_NOT_EXISTING

        player = current_players[uuid]
        s = player.current_session_id
        index = games.get_session(s)
        print 'INDEX: ', index

        correct = False
        if index is not None:
            #correct = my_session.update_game(msg, player)
            games.update_session(msg, index, player)

            #ic_update.publish_update(my_session)
        else:
            print("error: no session with id %d found!" % s)
            return protocol._RSP_NO_GAME_FOUND
        return protocol._ACK

    elif protocol.server_process(msg) == protocol._SA_LEAVE_SESSION:
        player = current_players[uuid]
        games.leave_session(player)
        return protocol._ACK

    elif msg == protocol._TERMINATOR:
        return



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
    games = GamesHandler(args)
    global shouldRunning
    threads = []

    # game server discovery beacon
    interval = 2   # 2 secs discovery_signal_interval
    t = threading.Thread(target=game_server_beacon, args=(interval,)).start()
    threads.append(t)

    # handling client requests
    rpcServer = RpcServer(request_handler=request_handler, handler_args=(games,))

    while True:
        try:
            sleep(1)
        except (KeyboardInterrupt, SystemExit):
            # clean-ups
            if threads:
                for thread in threads:
                    thread.join()  # FIXME: cannot join game server discovery thread.. why?
            break
    print("server ends.")

if __name__ == '__main__':
    server_main()