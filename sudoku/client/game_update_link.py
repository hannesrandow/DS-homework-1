"""
Will become redundant with publish/subscribe
"""




import pickle
import socket
import threading
from sudoku.common.protocol import GAME_UPDATE_PORT

HOST = '127.0.0.1'


class GameUpdateLink:
    """A class to handle update received from server to the client"""
    def __init__(self, serv_addr, gui=None, session=None):
        self.__gu_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threaddd = None
        self.__shouldRunning = True
        self.gui = gui
        self.serv_addr = serv_addr
        self.latest_game = session
        # print("game update link created")

    def game_updates_thread(self, player_id):
        # game updates (gu) socket
        # TODO: a timeout!!
        print("waiting for the link back connection..")
        self.__gu_sock.connect((self.serv_addr, GAME_UPDATE_PORT))
        d = pickle.dumps(player_id)
        self.__gu_sock.send(d)
        self.__gu_sock.settimeout(4)
        print("link back is made!")
        while self.__shouldRunning:
            try:

                game_session = self.__gu_sock.recv(10000)
                self.latest_game = pickle.loads(game_session)
                print("received a game update from server!")
                if self.gui: # call only for the gui version
                    print("about to update gui")
                    self.gui.update(self.latest_game)
            except (socket.timeout, socket.gaierror) as error:
                print "timeouty for link back"
                continue
            except:
                print("about to close the link back..")
                break
                # todo: game update

    def create(self, client_ip):
        print("specifier to create link back with: " , client_ip)
        if not self.threaddd:
            self.threaddd = \
                threading.Thread(target=self.game_updates_thread, args=(client_ip,)).start()
        else:
            print "Already created a link!"
            # TODO: print more details

    def destroy(self):
        if self.threaddd:
            self.__shouldRunning = False
            # FIXME: thread is not being closed correctly! something sucks about socket
            self.threaddd.join()
            self.threaddd = None
        self.__gu_sock.shutdown(2)
        self.__gu_sock.close()