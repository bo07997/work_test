# coding: UTF-8
import time
import json
import zmq
import zmq_test.Service.server_config as server_config
import random
import json
from zmq.eventloop import ioloop, zmqstream
from urllib.request import urlopen
context = zmq.Context()
ioloop.install()


class service:

    def __init__(self):
        self.ioloop = ioloop.IOLoop().instance()
        return

    def timeout(self):
        try:
            str = input("input:")
            self.socket_to_others.send_string("input", zmq.SNDMORE)
            self.socket_to_others.send_string(json.dumps({"cmd": str, "type": "cmd"}))
            self.ioloop.add_timeout(time.time() + 1, self.timeout)
        except Exception as err:
            pass

    def run(self):
        self.socket_to_others = server_config.context.socket(zmq.PUB)
        self.socket_to_others.connect(server_config.server_zmq_addr_accept)

        self.ioloop.add_timeout(time.time(), self.timeout)
        self.ioloop.start()
        return