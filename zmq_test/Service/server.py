import tornado
import tornado.ioloop
import tornado.web
import time
import multiprocessing
from ServerService import service as oneservice
from CilentService import service as twoservice
import zmq
context = zmq.Context()

def timeout():
    print ("timeout")
    return

def one():
    one = oneservice()
    one.run()
    return

def two():
    two = twoservice()
    two.run()
    return


if __name__ == "__main__":
    serviceone = multiprocessing.Process(target=one, args=())
    servicetwo = multiprocessing.Process(target=two, args=())
    servicetwo.start()
    serviceone.start()
    for p in multiprocessing.active_children():
        print("child p.name:" + p.name + "\tp.id" + str(p.pid))
