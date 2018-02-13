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

    def process_message_server(self, msg):
        print("get thread one message")
        print("processing .....", msg)
        return

    def timeout(self):
        try:
            str = input("input:")
            self.socket_to_others.send_string("input", zmq.SNDMORE)
            self.socket_to_others.send_string(json.dumps({"ip_cmd": str, "type": "cmd"}))
            self.ioloop.add_timeout(time.time() + 1, self.timeout)
        except Exception as err:
            pass

    def run(self):
        self.socket_to_others = server_config.context.socket(zmq.PUB)
        self.socket_to_others.connect(server_config.server_zmq_addr_accept)

        self.socket_from_server = server_config.context.socket(zmq.SUB)
        self.socket_from_server.connect(server_config.server_zmq_addr)
        self.socket_from_server.setsockopt_string(zmq.SUBSCRIBE, server_config.server_to_input_subject)
        self.stream_from_server_sub = zmqstream.ZMQStream(self.socket_from_server)
        self.stream_from_server_sub.on_recv(self.process_message_server)

        self.ioloop.add_timeout(time.time(), self.timeout)
        self.ioloop.start()
        return

if __name__ == '__main__':
    input_ = service()
    input_.run()