import pickle


class Player(object):
    def __init__(self, client_ip, nickname=None, current_session_id=None):
        self.client_ip = client_ip
        self.nickname = nickname
        self.current_session_id = current_session_id
        self.score = 0
        self.link_back_sock = None

    # avoid socket object to be picked: this bastard took me hours to solve
    def __getstate__(self):
        d = dict(self.__dict__)
        del d['link_back_sock']
        return d

    # update the game
    def change_game_state(self):
        pass

    def send_game_updates(self, session):
        """This method is called for every player when their game udpated"""
        pickle_session = pickle.dumps(session)
        if self.link_back_sock:
            print ("send update to ", self.nickname)
            self.link_back_sock.send(pickle_session)
        else:
            print("#### link back socket not existing! ####")

    def close(self):
        if self.link_back_sock:
            self.link_back_sock.close()