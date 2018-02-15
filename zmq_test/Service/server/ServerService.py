# coding: UTF-8
import time
import json
import zmq
import server_config
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
        self.clients = {}
        self.in_client = "server"
        return

    def process_message_client(self, msg):
        body = json.loads(bytes.decode(msg[1]))
        # from client heart
        if body["type"] == "heart":
            clients = json.loads(bytes.decode(msg[0]))
            ip = clients["ip"]
            if ip not in self.clients:
                self.clients[ip] = {}
                self.clients[ip]["time"] = time.time()
                self.clients[ip]["tag"] = bytes.decode(msg[0])
            else:
                self.clients[ip]["time"] = time.time()

            pass
        # from input t
        elif body["type"] == "cmd":
            # a = os.system(body["cmd"])
            ip_cmd = body["ip_cmd"]
            if self.in_client == "server":  # input to server
                temp_ip_cmd = body["ip_cmd"].split(" ", 1)
                if temp_ip_cmd[0] == "ls":
                    message = {}
                    message["type"] = "server_message"
                    if self.clients != {}:
                        message["clients"] = self.clients
                    self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                    self.socket_to_others.send_string(json.dumps(message))
                elif temp_ip_cmd[0] == "ssh":
                    if temp_ip_cmd[1] in self.clients:
                        self.in_client = self.clients[temp_ip_cmd[1]]['tag']
                        message = {}
                        message["type"] = "state"
                        message["state"] = temp_ip_cmd[1]
                        self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                        self.socket_to_others.send_string(json.dumps(message))
                    else:
                        message = {}
                        message["type"] = "error"
                        message["error"] = "no client is %s" % temp_ip_cmd[1]
                        self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                        self.socket_to_others.send_string(json.dumps(message))

                else:
                    message = {}
                    message["type"] = "error"
                    message["error"] = "sorry, server no this cmd"
                    self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                    self.socket_to_others.send_string(json.dumps(message))
                    return

            else:  # input to client
                temp_ip_cmd = body["ip_cmd"].split(" ", 1)
                if temp_ip_cmd[0] == "exit":
                    self.in_client = "server"
                    message = {}
                    message["type"] = "state"
                    message["state"] = "server"
                    self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                    self.socket_to_others.send_string(json.dumps(message))
                else:
                    try:
                        tag = self.in_client
                        self.socket_to_others.send_string(tag, zmq.SNDMORE)
                        self.socket_to_others.send_string(json.dumps({"type": "cmd", "cmd": ip_cmd}))
                    except Exception as err:
                        message = {}
                        message["type"] = "error"
                        message["error"] = "unexcept error is occur!"
                        self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
                        self.socket_to_others.send_string(json.dumps(message))
        # from client cmd_result
        elif body["type"] == "cmd_result":
            self.socket_to_others.send_string(server_config.server_to_input_subject, zmq.SNDMORE)
            self.socket_to_others.send_string(json.dumps(body))
        return

    def timeout(self):

        # self.socket_to_others.send_string(zmqconfig.server_to_client_subject, zmq.SNDMORE)
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
        self.stream_from_others_sub.on_recv(self.process_message_client)

        self.ioloop.add_timeout(time.time(), self.timeout)
        # application = tornado.web.Application(urls)
        # application.listen(8887)
        self.ioloop.start()
        return