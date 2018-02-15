#-*- coding: utf-8 -*-
import zmq

context = zmq.Context()
server_zmq_addr = "tcp://192.168.31.20:9001"
server_to_client_subject = "server_to_client_subject"
server_to_input_subject = "server_to_input_subject"

server_zmq_addr_accept = "tcp://192.168.31.20:9002"
client_to_server_subject = "client_to_server_subject"

