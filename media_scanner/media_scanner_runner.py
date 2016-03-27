import threading
from kamerie import dispatcher, zmq


class MediaScanner(threading.Thread):
    def __init__(self):
        super(MediaScanner, self).__init__()

    def __enter__(self):
        self.dispatcher = dispatcher.Dispatcher()
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://localhost:{port}".format(port=dispatcher.DEFAULT_PORT))
        self.dispatcher.start()

    def __exit__(self):
        self.subscriber.close()
        self.context.term()
        self.dispatcher.close()
