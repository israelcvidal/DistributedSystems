from Requisition import Requisition
import sys
import socket
import threading
import pickle


if __name__ == '__main__':
    if len(sys.argv) != 6:
        raise Exception(sys.argv[0] + " expect 5 arguments: server_id, port, num_1, num_2, op")

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    NUM_1 = float(sys.argv[3])
    NUM_2 = float(sys.argv[4])
    OP = sys.argv[5]

    # We create a new requisition and then serialize it
    requisition = Requisition(NUM_1, NUM_2, OP)
    requisition_serialized = pickle.dumps(requisition)

    # We create a socket, connect to the server and then send our requisition
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((HOST, PORT))
    tcp.send(requisition_serialized)

    # We wait for the response, deserialize it and then print the result.
    response = tcp.recv(1024)
    response = pickle.loads(response)
    print(str(NUM_1) + " " + str(requisition.get_op_symbol()) + " " + str(NUM_2) + " = " + str(response))
