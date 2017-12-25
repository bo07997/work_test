import tornado
import tornado.ioloop
import tornado.web
import time
import multiprocessing
from oneservice import service as oneservice
from twoservice import service as twoservice
from threeservice import service as threeservice
import zmq
context = zmq.Context()

def timeout():
    print "timeout"
    return

def one():
    one = oneservice()
    one.run()
    return

def two():
    two = twoservice()
    two.run()
    return

def three():
    three = threeservice()
    three.run()
    return

if __name__ == "__main__":
    serviceone = multiprocessing.Process(target=one, args=())
    servicetwo = multiprocessing.Process(target=two, args=())
    servicethree = multiprocessing.Process(target=three, args=())
    servicethree.start()
    servicetwo.start()
    serviceone.start()
    for p in multiprocessing.active_children():
        print("child p.name:" + p.name + "\tp.id" + str(p.pid))