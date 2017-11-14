import pickle


class Player(object):
    """
    When the client joins a session or creates a new one, the server creates a player instance.
    """
    def __init__(self, client_ip, nickname=None, current_session_id=None):
        """
        :param client_ip: IP and port of the client.
        :param nickname: The nickname that the user gave himself.
        :param current_session_id: The session that the user is currently in.
        """
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
        """
        This method is called for every player when their game udpated.
        :param session: The session that the player is currently in.
        :return: None
        """
        pickle_session = pickle.dumps(session)
        if self.link_back_sock:
            print ("send update to ", self.nickname)
            self.link_back_sock.send(pickle_session)
        else:
            print("#### link back socket not existing! ####")

    def close(self):
        """
        This method gets calles when the client disconnects.
        :return: None
        """
        if self.link_back_sock:
            self.link_back_sock.close()