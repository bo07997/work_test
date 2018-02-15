#-*- coding: utf-8 -*-
import zmq

context = zmq.Context()
server_zmq_addr = "tcp://127.0.0.1:9001"
server_to_client_subject = "server_to_client_subject"

server_zmq_addr_accept = "tcp://127.0.0.1:9002"
client_to_server_subject = "client_to_server_subject"
