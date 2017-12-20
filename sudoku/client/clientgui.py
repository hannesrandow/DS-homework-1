"""
This script handles the GUI for the user and communicates with the server.
"""


import pickle
import threading
import time
from socket import AF_INET, SOCK_STREAM, socket
import time
from xmlrpclib import ServerProxy

from sudoku.GUI.EnterServerAddressDialog import EnterServerAddressDialog
from sudoku.GUI.Gameplay import *
from sudoku.GUI.EnterNicknameDialog import *
from sudoku.GUI.MultiplayerGameDialog import *

address = None
global running
running = True


class ClientGUI:
    def __init__(self, args):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.current_game_state = None
        self.name = None
        self.player = None
        self.client_ip = None
        server = (args.server_addr, int(args.port))
        self.proxy = ServerProxy("https://%s:%d" % server, allow_none=True)
        self.update_thread = threading.Thread(target=self.update_game_status_in_intervals)

    def update_game_status_in_intervals(self):
        # TODO: needs a lock to not update game state during "real update" (when number is entered)
        global running
        while running:
            time.sleep(0.2)
            updated_game_state = self.proxy.get_game_state()
            if updated_game_state != self.current_game_state:
                self.current_game_state = updated_game_state
                # TODO: update gui somehow


    def leave_session(self):
        self.proxy.leave_session()
        global running
        running = False
        self.update_thread.join()
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
        change = self.proxy.update(self.player, row, col, value)
        gui.update(change)

    def create_session(self, game_name, max_num_players):
        # print("create session")
        return self.proxy.create_session(self.player, game_name, max_num_players)
        # new_session = self.send_request(protocol._REQ_CREATE_SESSION + protocol._MSG_FIELD_SEP +
        #                                 game_name + protocol._MSG_FIELD_SEP + max_num_players)
        # return new_session

    def get_current_sessions(self):
        return self.proxy.get_current_sessions()
        # current_sessions = self.send_request(protocol._REQ_CURRENT_SESSIONS)
        # return current_sessions

    def nickname(self, n):
        self.proxy.nickname(self.player, n)
        self.name = n

    def connect(self):
        self.player = self.proxy.connect(address)
        # self.send_request(protocol._REQ_INITIAL_CONNECT)

    def join_session(self, session_id):
        rsp = self.proxy.join_session(self.player, session_id)
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
    address = addressGUI.address
    client.connect()
    client.nickname(nicknameGUI.nickname)
    # Done: use Multiplayer Game Dialog to join existing session or create a new one
    m = MultiplayerGameDialog(client)
    # print("session created")

    if m.session:
        gameplayGUI = Gameplay(address, m.session, client)
    else:
        print("session is empty -- probably from multiplayerdialog")


if __name__ == '__main__':
    client_gui_main()