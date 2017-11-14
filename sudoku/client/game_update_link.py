import pickle
import socket
import threading
from sudoku.common.protocol import GAME_UPDATE_PORT

HOST = '127.0.0.1'


class GameUpdateLink:
    """A class to handle update received from server to the client"""
    def __init__(self, gui=None):
        self.__gu_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__thread = None
        self.__shouldRunning = True
        self.gui = gui
        # print("game update link created")

    def game_updates_thread(self, player_id):
        # game updates (gu) socket
        # TODO: a timeout!!
        print("waiting for the link back connection..")
        self.__gu_sock.connect((HOST, GAME_UPDATE_PORT))
        self.__gu_sock.send(player_id)
        print("link back is made!")
        while self.__shouldRunning:
            try:
                game_session = self.__gu_sock.recv(10000)
                latest_game = pickle.loads(game_session)
                print("received a game update from server!")
                if self.gui:
                    print("about to update gui")
                    self.gui.update(latest_game)
            except:
                continue
                # todo: game update

    def create(self, player_id):
        print(player_id)
        if not self.__thread:
            self.__thread = \
                threading.Thread(target=self.game_updates_thread, args=(player_id,)).start()
        else:
            print "Already created a link!"
            # TODO: print more details

    def destroy(self):
        if self.__thread:
            self.__shouldRunning = False
            self.__thread.join()
            self.__thread = None
        self.__gu_sock.close()