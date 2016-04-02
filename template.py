import logging
import threading
import zmq

import time
from zmq.eventloop.minitornado.ioloop import PeriodicCallback
from zmq.eventloop.zmqstream import ZMQStream
from zmq.green.eventloop import ioloop

from kamerie.dispatcher import dispatcher

DEFAULT_TX_PORT = 5555
DEFAULT_RX_PORT = 5556
KEEP_ALIVE_INTERVAL = 10  # secs

KEEP_ALIVE_SIGNAL = b"keep_alive"
TRUE_SIGNAL = b"true"
CLOSE_SIGNAL = b"connection_closed"
ACK_SIGNAL = b"ack"


class TemplatePlugin(object):
    def __init__(self, plugin_name, tx_port=DEFAULT_TX_PORT, rx_port=DEFAULT_RX_PORT):
        # Prepare instance
        self.name = plugin_name
        self.tx_port = tx_port
        self.rx_port = rx_port
        self.alive = True

        # Prepare puller
        self.context = zmq.Context()

        self.publisher = self.context.socket(zmq.REQ)
        self.responder = self.context.socket(zmq.REP)

        self.publisher.bind("tcp://*.%d" % self.tx_port)
        self.responder.bind("tcp://*.%d" % self.rx_port)

        self.publisher = ZMQStream(self.publisher)
        self.responder = ZMQStream(self.responder)

        self.responder.on_recv(self.on_message)
        self.keep_alive_periodic = PeriodicCallback(self.keep_alive, KEEP_ALIVE_INTERVAL * 1000)

        # Prepare logger
        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)

    def start(self):
        self.keep_alive_periodic.start()
        try:
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            pass

    def on_message(self, message):
        raise NotImplementedError

    def run(self):
        self._logger.info("Starting thread #{id}, name: {name}".format(id=self.thread_id, name=self.thread_name))
        while self.alive:
            self.keep_alive()

    def __exit__(self):
        self.close()

    def close(self):
        self._logger.info("Exiting thread #{id}, name: {name}".format(id=self.thread_id, name=self.thread_name))
        self.publisher.close()
        self.responder.close()
        self.context.term()
        self.alive = False

    def keep_alive(self):
        self._logger.info("Sent keep alive signal")
        self.publisher.send_multipart([KEEP_ALIVE_SIGNAL, TRUE_SIGNAL])
