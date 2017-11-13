import pickle
from socket import AF_INET, SOCK_STREAM, socket
from time import sleep

from sudoku.common import protocol
from sudoku.common.protocol import HOST, PORT
from sudoku.client.game_update_link import GameUpdateLink


class ClientTerminal:
    def __init__(self):
        self.gameUpdateLink = GameUpdateLink()
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.current_session = None
        self.client_specifier = "default"  # used by server to distinguish clients for matching up link backs
        # TODO: maybe it's better to use hash of client's IP:PORT!!

    def leave_session(self):
        # self.gameUpdateLink.destroy()
        pass

    def send_request(self, m):
        self.socket.sendall(m)
        rsp = self.socket.recv(10000)
        if rsp == protocol._ACK:
            return True
        elif rsp == protocol._RSP_SESSION_FULL:
            return False
        else:
            return pickle.loads(rsp)

    def update(self, user_action, current_session):
        user_action = user_action.split(' ')
        row = user_action[1]
        column = user_action[2]
        number = user_action[3]

        update_request = self.send_request(protocol._REQ_UPDATE_GAME + protocol._MSG_FIELD_SEP +
                                           row + protocol._MSG_FIELD_SEP + column + protocol._MSG_FIELD_SEP + number)

        # print update_request
        if update_request.game_state != current_session.game_state:
            print 'correct'
        else:
            print 'incorrect'

        return update_request

    def create_session(self, game_name, max_num_players):
        new_session = self.send_request(protocol._REQ_CREATE_SESSION + protocol._MSG_FIELD_SEP +
                                        game_name + protocol._MSG_FIELD_SEP + max_num_players)
        return new_session

    def get_current_sessions(self):
        current_sessions = self.send_request(protocol._REQ_CURRENT_SESSIONS)
        # print 'Currently availabel sessions are: '
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
        self.send_request(protocol._REQ_NICKNAME + protocol._MSG_FIELD_SEP + n)
        return

    def connect(self):
        self.send_request(protocol._REQ_INITIAL_CONNECT)
        return

    def join_session(self, user_action):
        session_id = user_action.split(' ')[1]
        rsp = self.send_request(protocol._REQ_JOIN_SESSION + protocol._MSG_FIELD_SEP + session_id)
        # print "---- rspns : ", rsp
        if type(rsp) != bool:
            return rsp
        else:
            return 'session full'

    def process_response(m):
        pass

    def run(self):
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
            self.gameUpdateLink.create(self.client_specifier)
            # print 'new session created'
        elif user_action.startswith('-printsession'):
            if not self.current_session:
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
            self.gameUpdateLink.create(self.client_specifier)
            # print "--- we're joined --- "
            # print rsp
            if type(rsp) == str:
                print 'incorrect response : ', rsp
            else:
                self.current_session = rsp
            # print "in the join: ", current_session
        elif user_action.startswith(protocol._TERMINATOR):
            self.send_request(protocol._TERMINATOR)

    def stop(self):
        self.gameUpdateLink.destroy()
        self.socket.close()


def client_terminal_main(args=None):
    client = ClientTerminal()
    client.connect()

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