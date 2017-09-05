from sys import exit
from sys import argv
from socket import *

if len(argv) != 4:
	exit("UDPClient: Error! Expect params are HOST, PORT and DATA. Try again!")

HOST   = argv[1]
PORT   = int(argv[2])
DATA   = argv[3]
BUFSIZ = 1024

ADDR = (HOST, PORT)

udp_client_socket = socket(AF_INET, SOCK_DGRAM)

udp_client_socket.setblocking(False)

#The value 0.7 is a random choice
udp_client_socket.settimeout(0.7)

udp_client_socket.sendto(bytes(DATA, 'utf-8'), ADDR)

print("Data sent to", ADDR, "waiting for reply...")

try:
	data, _ = udp_client_socket.recvfrom(BUFSIZ)

	print("Reply received:", data.decode("utf-8"))

except timeout:
	print("Timeout!")