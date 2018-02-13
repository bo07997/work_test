# coding: UTF-8
import time
import json
import zmq
import zmq_test.Service.client_config as client_config
import random
import json
from zmq.eventloop import ioloop, zmqstream
from urllib.request import urlopen
context = zmq.Context()
ioloop.install()

server_zmq_addr_accept = "tcp://127.0.0.1:9002"
server_zmq_addr = "tcp://127.0.0.1:9001"


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
            my_ip = self.GetOuterIP()
            if not hasattr(self, "tag"):
                map = {"ip": bytes.decode(my_ip), "random": random.randrange(0, 99999)}
                self.tag = map
                self.socket_from_server.setsockopt_string(zmq.SUBSCRIBE, json.dumps(self.tag))
            self.socket_to_others.send_string(json.dumps(self.tag), zmq.SNDMORE)
            self.socket_to_others.send_string(json.dumps({"type": "heart"}))
            self.ioloop.add_timeout(time.time() + 3, self.timeout)
            return
        except Exception as err:
            pass

    def GetOuterIP(self):
        my_ip = urlopen('http://ip.42.pl/raw').read()
        return my_ip

    def run(self):
        self.socket_to_others = client_config.context.socket(zmq.PUB)
        self.socket_to_others.connect(server_zmq_addr_accept)

        self.socket_from_server = client_config.context.socket(zmq.SUB)
        self.socket_from_server.connect(server_zmq_addr)
        self.socket_from_server.setsockopt_string(zmq.SUBSCRIBE, "temp")
        self.stream_from_server_sub = zmqstream.ZMQStream(self.socket_from_server)
        self.stream_from_server_sub.on_recv(self.process_message_server)

        self.ioloop.add_timeout(time.time(), self.timeout)
        self.ioloop.start()
        return