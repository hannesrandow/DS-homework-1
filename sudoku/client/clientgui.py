"""
This script handles the GUI for the user and communicates with the server.
"""


import pickle
from socket import AF_INET, SOCK_STREAM, socket

from sudoku.GUI.EnterServerAddressDialog import EnterServerAddressDialog
from sudoku.GUI.Gameplay import *
from sudoku.GUI.EnterNicknameDialog import *
from sudoku.GUI.MultiplayerGameDialog import *
from sudoku.common import protocol


class ClientGUI:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.name = None
        self.client_ip = None
        self.rpcClient = None
        self.server_ip = None
        self.ic_update_link = None  # initialized after multiplayerGameDialog

    def leave_session(self):
        pass

    '''
    def send_request(self, m):
        self.sock.sendall(m)
        rsp = self.sock.recv(10000)
        if rsp == protocol._ACK:
            return True
        elif rsp == protocol._RSP_SESSION_FULL:
            return False
        else:
            return pickle.loads(rsp)
    '''

    def update(self, gui, row, col, value, session, dummy_update=False):
        #print(session.game_id)
        if dummy_update: # analogous to the update('-') from clientterminal!
            m = protocol._INIT
        else:
            m = str(row) + protocol._MSG_FIELD_SEP + str(col) + protocol._MSG_FIELD_SEP + str(value)
        print("before update")
        # TODO: send the information of the to changing session (which session)
        update_request = self.rpcClient.call(protocol._REQ_UPDATE_GAME + protocol._MSG_FIELD_SEP + m)
        # if update_request.game_state != session.game_state:
            # to deselect in the gui (removing the cursor)
            # gui.row, gui.col = -1, -1
        print("after update..")
        # TODO: maybe we need this: update_request = pickle.loads(update_request)
        # just for information
        if update_request[1]:
            # TODO: update score +1
            print 'correct'
        else:
            # TODO: update score -1
            print 'incorrect'

        if dummy_update:
            return
        else:
            print("game should be updated by ICUpdate soon..")

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
        # print("create session")
        new_session = self.rpcClient.call(protocol._REQ_CREATE_SESSION + protocol._MSG_FIELD_SEP +
                                        game_name + protocol._MSG_FIELD_SEP + max_num_players)
        # new_session = pickle.loads(new_session)
        return new_session

    def get_current_sessions(self):
        current_sessions = self.rpcClient.call(protocol._REQ_CURRENT_SESSIONS)
        # FIXME: use sth different (do not encode here) [without it it does not work on Windows]
        return pickle.loads(current_sessions.encode("UTF-8"))

    def nickname(self, n):
        res = self.rpcClient.call(protocol._REQ_NICKNAME + protocol._MSG_FIELD_SEP + n)
        print(res)
        if res == protocol._RSP_OK:
            print("nickname accepted")
        else:
            print("nickname did not accepted!")  # TODO: print why not!
        self.name = n
        return

    def connect(self):
        res = self.rpcClient.call(protocol._REQ_INITIAL_CONNECT)
        if res == protocol._RSP_OK:
            print("connected successfuly!")
        else:
            print("some problem with connection!") # TODO: print why not!
        return

    def join_session(self, session_id):
        # print("join the session")
        rsp = self.rpcClient.call(protocol._REQ_JOIN_SESSION + protocol._MSG_FIELD_SEP + str(session_id))
        if type(rsp) != bool:
            return rsp
        else:
            if rsp == protocol._RSP_SESSION_FULL:
                return 'session full'
            else:
                return "UUID is not available"

    def process_response(self, m):
        pass


def client_gui_main(args=None):
    client = ClientGUI()

    nicknameGUI = EnterNicknameDialog()
    addressGUI = EnterServerAddressDialog(client)
    client.connect()
    client.nickname(nicknameGUI.nickname)
    # Done: use Multiplayer Game Dialog to join existing session or create a new one
    m = MultiplayerGameDialog(client)
    # print("session created")

    # TODO: address of addressGUI could be wrong
    gameplayGUI = Gameplay(addressGUI.address, str(m.gameName), client)


if __name__ == '__main__':
    client_gui_main()