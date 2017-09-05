from random import random
from time import sleep
from threading import Thread
from sys import exit
from sys import argv
from socket import *

# Set True if you want to generate possible timeouts in local network
TEST_TIMEOUT = False

if len(argv) != 2:
	exit("UDPServer: Error! Expect param is PORT. Try again!")

HOST   = "localhost"
BUFSIZ = 1024
PORT   = int(argv[1])
ADDR   = (HOST, PORT)

class Executor(Thread):
	def __init__(self, data, client_addr):
		super(Executor, self).__init__()
		self._data = data.decode("utf-8")
		self._client_addr = client_addr

	def run(self):
		if TEST_TIMEOUT: sleep(random())

		data = self._data[::-1]
		udp_socket = socket(AF_INET, SOCK_DGRAM)
		udp_socket.sendto(bytes(data, "utf-8"), self._client_addr)
		udp_socket.close()

udp_server_sock = socket(AF_INET, SOCK_DGRAM)
udp_server_sock.bind(ADDR)

while True:
	print("Waiting for data...")

	data, client_addr = udp_server_sock.recvfrom(BUFSIZ)
	Executor(data, client_addr).start()

	print("Data received from", client_addr)

udp_server_sock.close()