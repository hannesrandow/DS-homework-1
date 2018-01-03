import pika
import pickle
import threading
"""
Publish/subscribe scenario to receive updates to the game from the server.
On client side.
"""
class ICUpdate_link:

    def __init__(self, game_name, gui=None, session=None):
        #incidently the same name as the game
        self.game_name = game_name
        self.threaddd = None
        self.__shouldRunning = True
        self.gui = gui
        self.latest_game = session
        # TODO***: use IP variable/parameter to get connected!
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.game_name,
                                      exchange_type='fanout')
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.game_name,
                                queue=queue_name)
        self.channel.basic_consume(self.callback,
                                   queue=queue_name,
                                   no_ack=True)
        # threading.Thread.__init__(self)
        # self.start()
        self.main()

    def main(self):
        print('Sudoku game %s running on client...' % self.game_name)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, game_session):
        """
        Probably will have to pickle game_session, since callback takes a string here.
        Receive the updates from the server and update the game accordingly.

        Have to add a check here, to update gui only if there is a change?
        :param ch:
        :param method:
        :param properties:
        :param latest_game:
        :return: None
        """
        self.latest_game = pickle.loads(game_session)
        print 'callback'
        if self.gui:  # call only for the gui version
            print("about to update gui")
            # FIXME***: I think we need to activate a flag in GamePlay that calls following update
            # because otherwise we get something related to main loop issue
            self.gui.update(self.latest_game)
        else:
            for row in self.latest_game.game_state:
                print row
        return

