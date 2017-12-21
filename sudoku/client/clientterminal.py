"""
This script handles all the actions the client can make and communicates with the server from the terminal.
"""

import pickle
from time import sleep

from sudoku.client.game_server_discovery import GameServerDiscovery
from sudoku.client.rpc_client import RpcClient
from sudoku.common import protocol
from sudoku.client.ic_update_link import ICUpdate_link


class ClientTerminal:
    def __init__(self):
        self.current_session = None
        self.client_specifier = "default"  # used by server to distinguish clients for matching up link backs
        self.update_link = None
        self.rpcClient = None

    def leave_session(self):
        # self.gameUpdateLink.destroy()
        pass

    def update(self, user_action, current_session):
        """
        This method allows the user to make a change to the sudoku game.
        :param user_action: Contains the row and column where the user makes the change, as well as the new number.
        :param current_session: The session that the client is currently in.
        :return: The response from the server whether the update was correct or incorrect.
        """
        user_action = user_action.split(' ')
        row = user_action[1]
        column = user_action[2]
        number = user_action[3]

        update_request = self.rpcClient.call(protocol._REQ_UPDATE_GAME + protocol._MSG_FIELD_SEP +
                                           row + protocol._MSG_FIELD_SEP + column + protocol._MSG_FIELD_SEP + number)

        update_request = pickle.loads(update_request)
        if update_request[1] == True:
            print 'correct'
        else:
            print 'incorrect'
        return update_request[0]

    def create_session(self, game_name, max_num_players):
        """
        This method allows the user to create a new session.
        :param game_name: The name that the session should have.
        :param max_num_players: The maximum number of players that can be in the session.
        :return: The created session, from the server.
        """
        # new_session = self.send_request(protocol._REQ_CREATE_SESSION + protocol._MSG_FIELD_SEP +
        #                                 game_name + protocol._MSG_FIELD_SEP + max_num_players)

        new_session = self.rpcClient.call(protocol._REQ_CREATE_SESSION + protocol._MSG_FIELD_SEP +
                                        game_name + protocol._MSG_FIELD_SEP + max_num_players)

        return new_session

    def get_current_sessions(self):
        """
        Allows the user to view all the sessions that are currently running on the server.
        """
        #get current sessions from server
        current_sessions = self.rpcClient.call(protocol._REQ_CURRENT_SESSIONS)
        # FIXME: use sth different (do not encode here) [without it it does not work on Windows]
        current_sessions = pickle.loads(current_sessions.encode("UTF-8"))

        for session in current_sessions:
            print
            '------------------ SESSION ---------------------'
            print session.game_name
            print session.game_id
            print ' '.join([player.nickname for player in session.current_players])  # session.current_players
            print session.max_num_of_players
            print
            '------------------ SESSION ---------------------'

    def nickname(self, n):
        """
        Allows the user to specify a nickname/username for himself
        :param n: The desired nickname/username
        :return: None
        """
        # self.send_request(protocol._REQ_NICKNAME + protocol._MSG_FIELD_SEP + n)
        res = self.rpcClient.call(protocol._REQ_NICKNAME + protocol._MSG_FIELD_SEP + n)
        print(res)
        if res == protocol._RSP_OK:
            print("nickname accepted")
        else:
            print("nickname did not accepted!") # TODO: print why not!
        return

    def connect(self, serv_addr='localhost'):
        """
        This method is called for the initial connect between the client and the server.
        :return: None
        """
        # self.send_request(protocol._REQ_INITIAL_CONNECT)
        try:
            self.rpcClient = RpcClient(serv_addr)
        except Exception as e:
            print('could not establish connected with the RabbitMQ server: %s' % e)
            exit(-1)

        res = self.rpcClient.call(protocol._REQ_INITIAL_CONNECT)
        if res == protocol._RSP_OK:
            print("connected successfuly!")
        else:
            print("some problem with connection!") # TODO: print why not!
        return

    def join_session(self, user_action):
        """
        This method allows the user to join one of the existing sessions.
        :param user_action: The id of the session the user wants to join
        :return: The session that the user joined, or a message saying that the session has reached its maximum
        number of players
        """
        session_id = user_action.split(' ')[1]
        rsp = self.rpcClient.call(protocol._REQ_JOIN_SESSION + protocol._MSG_FIELD_SEP + session_id)
        # TODO: use simpler output for the joining session (on server!)
        if type(rsp) != bool:
            return rsp
        else:
            if rsp == protocol._RSP_SESSION_FULL:
                return 'session full'
            else:
                return "UUID is not available"

    def find_self(self):
        """
        Find the representation of the client in current players of the session.
        E.g. to get score.
        :return: The player instance in the current players of the session.
        """
        for p in self.current_session.current_players:
            if p.client_ip == self.socket.getsockname():
                return p

    def run(self):
        """
        This method processes all the user actions from the terminal.
        :return: None
        """
        print "client running.."
        user_action = raw_input('enter action preceded by -flag: ')
        if user_action.startswith('-username'):
            nickname = user_action.split(' ')[1]
            self.client_specifier = nickname
            self.nickname(nickname)
            print 'username created'
        elif user_action.startswith('-newsession'):
            # current_session = create_session('test_game', '5')
            user_input = user_action.split(' ')
            self.current_session = self.create_session(user_input[1], user_input[2])
            # print 'new session created'
        elif user_action.startswith('-printsession'):
            #if not self.current_session:
            if self.current_session:
                for i in self.current_session.game_state:
                    print i
            else:
                print("no session exists!")
        elif user_action.startswith('-getsessions'):
            self.get_current_sessions()
        elif user_action.startswith('-update'):
            self.current_session = self.update(user_action, self.current_session)
        elif user_action.startswith('-solution'):
            inf = user_action.split(' ')
        elif user_action.startswith('-join'):
            rsp = self.join_session(user_action)
            # self.gameUpdateLink.create(self.socket.getsockname())
            # TODO: self.update_link = ICUpdate_link(rsp.game_name or sth similar)
            # print "--- we're joined --- "
            # print rsp
            if type(rsp) == str:
                print 'incorrect response : ', rsp
            else:
                self.current_session = rsp
            # print "in the join: ", current_session
        elif user_action.startswith('-score'):
            #score = self.current_session.current_players[0].score
            if self.current_session:
                score = self.find_self().score
                print 'my score is: ', score
            else: 
                print "currenty not in a session"
        # elif user_action.startswith('-sn'):
        #     print self.socket.getsockname()
        elif user_action.startswith(protocol._TERMINATOR):
            self.send_request(protocol._TERMINATOR)

    def stop(self):
        """
        Destroy the connection.
        :return: None
        """
        self.gameUpdateLink.destroy()
        self.socket.shutdown(2)
        self.socket.close()


def client_terminal_main(args=None):
    serv_addr = raw_input("Enter server address (or 'auto'): ")
    if serv_addr == 'auto':
        game_server_discovery = GameServerDiscovery()
        print("found: ", game_server_discovery.get_list())
        serv_addr = game_server_discovery.get_list().pop(0)
        game_server_discovery.stop()
    print("connecting to %s .." % serv_addr)

    client = ClientTerminal()
    client.connect(serv_addr)
    # FIXME: some considerations required for rabbitmq for remote ip connection: http://bit.ly/2z4lwZY

    while True:
        sleep(1)
        try:
            client.run()
        except KeyboardInterrupt as e:
            client.stop()
            print("terminated!")
            exit(-1)


if __name__ == '__main__':
    client_terminal_main()