# coding: UTF-8
import time
import zmq
import input_config
import json
from zmq.eventloop import ioloop, zmqstream
context = zmq.Context()
ioloop.install()


class service:

    def __init__(self):
        self.ioloop = ioloop.IOLoop().instance()
        self.state = "server"
        return

    def process_message_server(self, msg):
        body = json.loads(bytes.decode(msg[1]))
        if body["type"] == "server_message":
            print("------------------------------------------------------------------")
            print("ip                                               time")
            if "clients" not in body:
                return
            for ip in body["clients"]:
                time_array = time.localtime(body["clients"][ip]["time"])
                result_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                print("%s                                  %s" % (ip, result_time))
        elif body["type"] == "error":
            print(body["error"])
        elif body["type"] == "cmd_result":
            if body["cmd_result"] != "":
                print(body["cmd_result"])
            else:
                print("------------------------------------------------------------------")
                if body["code"] == 0:
                    print("success")
                else:
                    print("sorry, error is occur")
        elif body["type"] == "state":
            self.state = body["state"]
        return

    def timeout(self):
        try:
            str_input = input("%s:" % self.state)
            self.socket_to_others.send_string("input", zmq.SNDMORE)
            self.socket_to_others.send_string(json.dumps({"ip_cmd": str_input, "type": "cmd"}))
            self.ioloop.add_timeout(time.time() + 1, self.timeout)
        except Exception as err:
            pass

    def run(self):
        self.socket_to_others = input_config.context.socket(zmq.PUB)
        self.socket_to_others.connect(input_config.server_zmq_addr_accept)

        self.socket_from_server = input_config.context.socket(zmq.SUB)
        self.socket_from_server.connect(input_config.server_zmq_addr)
        self.socket_from_server.setsockopt_string(zmq.SUBSCRIBE, input_config.server_to_input_subject)
        self.stream_from_server_sub = zmqstream.ZMQStream(self.socket_from_server)
        self.stream_from_server_sub.on_recv(self.process_message_server)

        self.ioloop.add_timeout(time.time(), self.timeout)
        self.ioloop.start()
        return


if __name__ == '__main__':
    input_ = service()
    input_.run()