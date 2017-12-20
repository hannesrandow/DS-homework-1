import pickle


class Player(object):
    """
    When the client joins a session or creates a new one, the server creates a player instance.
    """
    def __init__(self, uuid, nickname=None, current_session_id=None):
        """
        :param uuid: universal id for the client (same used from rabbitMQ)
        :param nickname: The nickname that the user gave himself.
        :param current_session_id: The session that the user is currently in.
        """
        self.uuid = uuid
        self.nickname = nickname
        self.current_session_id = current_session_id
        self.score = 0

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
        # TODO: use RabbitMQ publish/subscriber to send the updates to the user
        # if self.link_back_sock:
        #     print ("send update to ", self.nickname)
        #     self.link_back_sock.send(pickle_session)
        # else:
        #     print("#### link back socket not existing! ####")

    def close(self):
        """
        This method gets calles when the client disconnects.
        :return: None
        """
        # TODO: maybe doing rabbitmq cleanups here!
        pass