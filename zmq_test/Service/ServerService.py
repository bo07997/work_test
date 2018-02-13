# coding: UTF-8
import time
import json
import zmq
import zmqconfig
from zmq.eventloop import ioloop, zmqstream
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.ioloop import ZMQIOLoop
#ioloop.install()
#application = tornado.web.Application(urls)
class service:

    def __init__(self):
        self.ioloop = ZMQIOLoop()
        self.ioloop.install()
        self.cilents = {}
        return

    def process_message_cilent(self, msg):
        body = json.loads(bytes.decode(msg[1]))
        if body["type"] == "heart":
            self.cilents[bytes.decode(msg[0])] = time.time()
            pass
        return

    def timeout(self):

        # self.socket_to_others.send_string(zmqconfig.server_to_cilent_subject, zmq.SNDMORE)
        # self.socket_to_others.send_string(json.dumps(""))
        self.ioloop.add_timeout(time.time() + 3, self.timeout)
        return

    def run(self):
        self.socket_to_others = zmqconfig.context.socket(zmq.PUB)
        self.socket_to_others.bind(zmqconfig.server_zmq_addr)

        # 服务端收信息,不同机子
        self.socket_from_others = zmqconfig.context.socket(zmq.SUB)
        self.socket_from_others.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket_from_others.bind(zmqconfig.server_zmq_addr_accept)
        self.stream_from_others_sub = zmqstream.ZMQStream(self.socket_from_others)
        self.stream_from_others_sub.on_recv(self.process_message_cilent)

        self.ioloop.add_timeout(time.time(), self.timeout)
        # application = tornado.web.Application(urls)
        # application.listen(8887)
        self.ioloop.start()
        return