# coding: UTF-8
import time
import json
import zmq
import zmq_test.Service.server_config as server_config
from zmq.eventloop import ioloop, zmqstream
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.ioloop import ZMQIOLoop
import re
import sys
import os
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
            cilent = json.loads(bytes.decode(msg[0]))
            ip = cilent["ip"]
            if ip not in self.cilents:
                self.cilents[ip] = {}
                self.cilents[ip]["time"] = time.time()
                self.cilents[ip]["tag"] = bytes.decode(msg[0])
            else:
                self.cilents[ip]["time"] = time.time()

            pass
        elif body["type"] == "cmd":
            # a = os.system(body["cmd"])
            ip_cmd = body["ip_cmd"].split(" ")
            if len(ip_cmd) == 1:  # input to server
                self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                message = "no cilents"
                if self.cilents != {}:
                    message = json.dumps(self.cilents)
                self.socket_to_others.send_string(message)
            else:  # from input
                try:
                    tag = None
                    if ip_cmd[0] in self.cilents:  # input to cilent
                        tag = self.cilents[ip_cmd[0]]["tag"]
                        self.socket_to_others.send_string(tag, zmq.SNDMORE)
                        self.socket_to_others.send_string(json.dumps({"type": "cmd", "cmd": ip_cmd[1]}))
                    else:
                        self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                        self.socket_to_others.send_string("cmd is error,example like 110.110.110.110 ls")
                except Exception as err:
                    self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                    self.socket_to_others.send_string("unexcept error is occur!")
        return

    def timeout(self):

        # self.socket_to_others.send_string(zmqconfig.server_to_cilent_subject, zmq.SNDMORE)
        # self.socket_to_others.send_string(json.dumps(""))
        self.ioloop.add_timeout(time.time() + 3, self.timeout)
        return

    def run(self):
        self.socket_to_others = server_config.context.socket(zmq.PUB)
        self.socket_to_others.bind(server_config.server_zmq_addr)

        # 服务端收信息,不同机子
        self.socket_from_others = server_config.context.socket(zmq.SUB)
        self.socket_from_others.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket_from_others.bind(server_config.server_zmq_addr_accept)
        self.stream_from_others_sub = zmqstream.ZMQStream(self.socket_from_others)
        self.stream_from_others_sub.on_recv(self.process_message_cilent)

        self.ioloop.add_timeout(time.time(), self.timeout)
        # application = tornado.web.Application(urls)
        # application.listen(8887)
        self.ioloop.start()
        return