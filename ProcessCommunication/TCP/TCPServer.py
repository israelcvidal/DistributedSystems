A from Requisition import Requisition
import sys
import socket
import threading
import pickle
import time
import logging


def execute(socket_, client_):
    """This function must be executed in a new thread so the server can receive requisitions concurrently"""

    # recv expects the maximum buffer size
    requisition = socket_.recv(1024)
    requisition_deserialized = pickle.loads(requisition)

    op = requisition_deserialized.op
    num_1 = requisition_deserialized.num_1
    num_2 = requisition_deserialized.num_2
    # time.sleep(10)

    # Here we get the response that will be send to the client
    if op == "soma":
        response = num_1 + num_2
    elif op == "multi":
        response = num_1 * num_2

    elif op == "div":
        response = num_1 / num_2

    elif op == "sub":
        response = num_1 - num_2

    else:
        raise TypeError("'op' must be one of the following: " + ", ".join(Requisition.valid_options))

    # We serialize the response and then send it through the socket
    response = pickle.dumps(response)
    socket_.send(response)
    socket_.close()
    # After closing the socket we log the operation on file
    logging.info("[" + str(num_1) + " " + str(num_2) + " " + str(op) + "]" + "[" + str(client_[0]) + "]")


if __name__ == '__main__':
    logging.basicConfig(filename='log.log', level=logging.INFO)

    if len(sys.argv) != 2:
        raise Exception(sys.argv[0] + " expect 1 argument: Server port")

    PORT = int(sys.argv[1])
    HOST = ''
    # We open a socket and start listening on it
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind((HOST, PORT))
    tcp.listen(1)

    while True:
        # When a client opens a requisition, we accept it and then start a new thread to respond to it.
        socket, client = tcp.accept()
        threading.Thread(target=execute, args=[socket, client]).start()


