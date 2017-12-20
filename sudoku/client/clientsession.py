import pika

class ClientSession:

    def __init__(self, game_name):
        #incidently the same name as the game
        self.game_name = game_name
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
        self.main()

    def main(self):
        print('Sudoku game %s running...' % self.game_name)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print('\n          %s\n' % body)
        return