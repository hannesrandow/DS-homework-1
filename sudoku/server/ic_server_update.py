import pika
import pickle

"""
Here the server will send updates to the sudoku game to the clients that are subscribed to the game.
"""

class ICServerUpdate:


    def __init__(self, game_name, session):
        self.game_name = game_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.game_name,
                                      exchange_type='fanout')
        self.session = session
        print('Sudoku game %s running...' % self.game_name)
        self.users = []

    def add_user(self, username):
        self.users.append(username)
        return

    def remove_user(self, username):
        self.users.remove(username)
        return

    def publish_update(self, update):
        update = pickle.dumps(update)
        print('published update')
        self.channel.basic_publish(exchange=self.game_name,
                                   routing_key='',
                                   body=update)
        if len(self.users) == 0:
            self.delete_game()
        return

    def delete_game(self):
        """
        TODO: announce winner before game is deleted
        :return:
        """
        self.channel.close()
        self.connection.close()
        return
