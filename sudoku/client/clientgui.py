"""
This script handles the GUI for the user and communicates with the server.
"""


import pickle
from socket import AF_INET, SOCK_STREAM, socket
import time
from xmlrpclib import ServerProxy

from sudoku.GUI.EnterServerAddressDialog import EnterServerAddressDialog
from sudoku.GUI.Gameplay import *
from sudoku.GUI.EnterNicknameDialog import *
from sudoku.GUI.MultiplayerGameDialog import *


class ClientGUI:
    def __init__(self, args):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.name = None
        self.client_ip = None
        server = (args.server_addr, int(args.port))
        self.proxy = ServerProxy("https://%s:%d" % server, allow_none=True)

    def leave_session(self):
        self.proxy.leave_session()
        # Why was just a pass here before?

# should not be necessary anymore
    # def send_request(self, m):
    #     self.sock.sendall(m)
    #     rsp = self.sock.recv(10000)
    #     if rsp == protocol._ACK:
    #         return True
    #     elif rsp == protocol._RSP_SESSION_FULL:
    #         return False
    #     else:
    #         return pickle.loads(rsp)

    def update(self, gui, row, col, value, session):
        change = self.proxy.update(row, col, value)
        gui.update(change)

    def create_session(self, game_name, max_num_players):
        # print("create session")
        return self.proxy.create_session(game_name, max_num_players)
        # new_session = self.send_request(protocol._REQ_CREATE_SESSION + protocol._MSG_FIELD_SEP +
        #                                 game_name + protocol._MSG_FIELD_SEP + max_num_players)
        # return new_session

    def get_current_sessions(self):
        return self.proxy.get_current_sessions()
        # current_sessions = self.send_request(protocol._REQ_CURRENT_SESSIONS)
        # return current_sessions

    def nickname(self, n):
        self.proxy.nickname(n)
        self.name = n

    def connect(self):
        self.proxy.connect()
        # self.send_request(protocol._REQ_INITIAL_CONNECT)

    def join_session(self, session_id):
        rsp = self.proxy.join_session(session_id)
        # print("join the session")
        # rsp = self.send_request(protocol._REQ_JOIN_SESSION + protocol._MSG_FIELD_SEP + str(session_id))
        if type(rsp) != bool:
            return rsp
        else:
            return 'session full'

    def process_response(self, m):
        pass


def client_gui_main(args=None):
    client = ClientGUI(args)

    nicknameGUI = EnterNicknameDialog()
    addressGUI = EnterServerAddressDialog(client)
    client.connect()
    client.nickname(nicknameGUI.nickname)
    # Done: use Multiplayer Game Dialog to join existing session or create a new one
    m = MultiplayerGameDialog(client)
    # print("session created")

    if m.session:
        gameplayGUI = Gameplay(addressGUI.address, m.session, client)
    else:
        print("session is empty -- probably from multiplayerdialog")


if __name__ == '__main__':
    client_gui_main()