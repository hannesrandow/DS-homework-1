import threading

import pika
import uuid

# using example from https://www.rabbitmq.com/tutorials/tutorial-six-python.html
class RpcClient(threading.Thread):
    """ A client that runs on so called rabbitMQ RPC queue """
    def __init__(self, rabbitmq_addr):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_addr))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.corr_id = str(uuid.uuid4())
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        """ is called when a reply is received in response to the call """
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, msg):
        """ the call to a remote method is occurred here """
        self.response = None
        print("uuid: ", self.corr_id)
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(msg))
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode("utf-8")


if __name__ == "__main__":
    # run this test with rpc_server test
    rpc = RpcClient()
    print(rpc.call(3))