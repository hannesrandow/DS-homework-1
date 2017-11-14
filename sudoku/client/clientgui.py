import pickle
from socket import AF_INET, SOCK_STREAM, socket
from sudoku.GUI.Gameplay import *
from sudoku.GUI.EnterNicknameDialog import *
from sudoku.GUI.MultiplayerGameDialog import *
from sudoku.common import protocol
from sudoku.common.protocol import HOST, PORT
from sudoku.client.game_update_link import GameUpdateLink



class ClientGUI:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        self.gameplayGUI = None

    def leave_session(self):
        pass

    def send_request(self, m):
        self.sock.sendall(m)
        rsp = self.sock.recv(10000)
        if rsp == protocol._ACK:
            return True
        elif rsp == protocol._RSP_SESSION_FULL:
            return False
        else:
            return pickle.loads(rsp)

    def update(self, gui, row, col, value, session):
        #print(session.game_id)
        # TODO: send the information of the to changing session (which session)
        update_request = self.send_request(protocol._REQ_UPDATE_GAME + protocol._MSG_FIELD_SEP +
                                           str(row) + protocol._MSG_FIELD_SEP + str(col) + protocol._MSG_FIELD_SEP + str(value))
        # if update_request.game_state != session.game_state:
            # to deselect in the gui (removing the cursor)
            # gui.row, gui.col = -1, -1
        if update_request[1]:
            # TODO: update score +1
            print 'correct'
        else:
            # TODO: update score -1
            print 'incorrect'

        gui.update(update_request[0])

    '''
    def update(self, user_action, current_session):
        user_action = user_action.split(' ')
        row = user_action[1]
        column = user_action[2]
        number = user_action[3]

        update_request = self.send_request(protocol._REQ_UPDATE_GAME + protocol._MSG_FIELD_SEP +
                                           row + protocol._MSG_FIELD_SEP + column + protocol._MSG_FIELD_SEP + number)

        if update_request.game_state != current_session.game_state:
            print 'correct'
        else:
            print 'incorrect'

        return update_request
    '''

    def create_session(self, game_name, max_num_players):
        new_session = self.send_request(protocol._REQ_CREATE_SESSION + protocol._MSG_FIELD_SEP +
                                        game_name + protocol._MSG_FIELD_SEP + max_num_players)
        if self.gameplayGUI:
            self.gameUpdateLink = GameUpdateLink(self.gameUpdateLink)
            self.gameUpdateLink.create(self.nickname)

        return new_session

    def get_current_sessions(self):
        current_sessions = self.send_request(protocol._REQ_CURRENT_SESSIONS)
        return current_sessions

    def nickname(self, n):
        self.send_request(protocol._REQ_NICKNAME + protocol._MSG_FIELD_SEP + n)
        self.nickname = n
        return

    def connect(self):
        self.send_request(protocol._REQ_INITIAL_CONNECT)
        return

    def join_session(self, user_action):
        session_id = user_action.split(' ')[1]
        rsp = self.send_request(protocol._REQ_JOIN_SESSION + protocol._MSG_FIELD_SEP + session_id)
        if type(rsp) != bool:
            if self.gameplayGUI:
                self.gameUpdateLink = GameUpdateLink(self.gameUpdateLink)
                self.gameUpdateLink.create(self.nickname)
            return rsp
        else:
            return 'session full'

    def process_response(self, m):
        pass


def client_gui_main(args=None):
    client = ClientGUI()
    client.connect()

    e = EnterNicknameDialog()
    client.nickname(e.nickname)
    # TODO: use Enter Address Dialog to get the server address
    # Done: use Multiplayer Game Dialog to join existing session or create a new one
    m = MultiplayerGameDialog(client)
    try:
        current_session = client.create_session(m.name, m.number)
    except:
        current_session = client.create_session(m.currentSession.game_name, str(m.currentSession.max_num_of_players))
    gameplayGUI = Gameplay(current_session, client)
    client.gameplayGUI = gameplayGUI

if __name__ == '__main__':
    client_gui_main()