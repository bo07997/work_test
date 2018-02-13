import time
import multiprocessing
from zmq_test.Service.ServerService import service as serverService
from zmq_test.Service.CilentService import service as cilentService
from zmq_test.Service.input import service as inputService
import zmq
context = zmq.Context()


def server():
    server = serverService()
    server.run()
    return


def cilent():
    cilent = cilentService()
    cilent.run()
    return


if __name__ == "__main__":
    server_Service = multiprocessing.Process(target=server, args=())
    cilent_Service = multiprocessing.Process(target=cilent, args=())
    server_Service.start()
    cilent_Service.start()
    for p in multiprocessing.active_children():
        print("child p.name:" + p.name + "\tp.id" + str(p.pid))
