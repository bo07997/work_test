#-*- coding: utf-8 -*-
import zmq

context = zmq.Context()
one_zmq_addr = "inproc://one_zmq_addr"
one_to_two_subject = "one_to_two_subject"
one_to_three_subject = "one_to_three_subject"

two_zmq_addr = "inproc://two_zmq_addr"
two_to_one_subject = "two_to_one_subject"
two_to_three_subject = "two_to_three_subject"

three_zmq_addr = "inproc://three_zmq_addr"
three_to_one_subject = "three_to_one_subject"
three_to_two_subject = "three_to_two_subject"

skin_zmq_addr = "tcp://127.0.0.1:8002"
skin_username = "ZGuard"
skin_password = "jz_hhj@#$"

test_zmq_addr = "tcp://192.168.58.128:8002"
subject = "test"