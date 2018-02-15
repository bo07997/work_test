import multiprocessing
from ClientService import service as clientService
import zmq
context = zmq.Context()


def client():
    client = clientService()
    client.run()
    return


if __name__ == "__main__":
    client_Service = multiprocessing.Process(target=client, args=())
    client_Service.start()
    for p in multiprocessing.active_children():
        print("child p.name:" + p.name + "\tp.id" + str(p.pid))
