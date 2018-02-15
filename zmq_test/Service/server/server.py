import multiprocessing
from ServerService import service as serverService
import zmq
context = zmq.Context()


def server():
    server = serverService()
    server.run()
    return


if __name__ == "__main__":
    server_Service = multiprocessing.Process(target=server, args=())
    server_Service.start()
    for p in multiprocessing.active_children():
        print("child p.name:" + p.name + "\tp.id" + str(p.pid))
