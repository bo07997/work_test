#-*- coding: utf-8 -*-
import zmq

context = zmq.Context()
server_zmq_addr = "tcp://127.0.0.1:9001"
server_to_cilent_subject = "server_to_cilent_subject"
server_to_input_subject = "server_to_input_subject"

server_zmq_addr_accept = "tcp://127.0.0.1:9002"
cilent_to_server_subject = "cilent_to_server_subject"

