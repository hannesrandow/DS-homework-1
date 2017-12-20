import threading
import pika


# using example from https://www.rabbitmq.com/tutorials/tutorial-six-python.html
class RpcServer(threading.Thread):
    """ A server that runs on so called rabbitMQ RPC queue handling """
    def __init__(self, test=False, start=True, request_handler=None, handler_args=None):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpc_queue')
        self.isRunning = True
        threading.Thread.__init__(self)
        if start:   # to start the thread automatically or by the caller signal
            self.start()
        self.threads = []   # multiple threads may be utilized other than the main thread to be responsive to the users requests
        self.test = test    # this method is called for test
        self.request_handler = request_handler  # this function is used to dispatched incoming requests
        self.handler_args = handler_args

    def run(self):
        """ Main thread of the RpcServer """
        print("RPC Server running.")
        # while self.isRunning and self.channel.queue_declare(queue='rpc_queue').method.message_count:
        # TODO: increase number of threads adaptively to the number of request!
        self.channel.basic_qos(prefetch_count=1)
        if self.test:
            self.channel.basic_consume(self.on_request_test, queue='rpc_queue')
        else:
            self.channel.basic_consume(self.on_request, queue='rpc_queue')
        self.channel.start_consuming()

    def fib(self, n):
        """ A test function call """
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n - 1) + self.fib(n - 2)

    def on_request_test(self, ch, method, props, body):
        """ A test request handling """
        n = int(body)

        print(" [.] fib(%s)" % n)
        response = self.fib(n)
        print("  \--------- %s " % response)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def on_request(self, ch, method, props, body):
        """ handles an incoming request """
        response = "none"
        if self.request_handler:
            response = self.request_handler(body, props.correlation_id, self.handler_args)
        else:
            # TODO: better error handling and reporting
            print("[RPCServer] error: request_handler is None!")

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def stop(self):
        """ stops the rpc handler thread and closes connection """
        self.isRunning = False
        self.join()
        self.connection.close()


if __name__ == "__main__":
    print("stand alone test here.")
    rpc = RpcServer(test=True, start=False)
    rpc.start()
