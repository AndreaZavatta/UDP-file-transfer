import os
import pickle
import select
from time import sleep

from settings import *
from socket import *


def get_number_of_packets():
    while True:
        try:
            data = server_socket.recv(BUFFER_SIZE)
            if data:
                n = int(data.decode())
                return n
        except error:
            pass


def receive_file(fn):
    server_socket.sendto('ACK'.encode(), client_address)
    packets = []
    for i in range(num):
        data = server_socket.recv(BUFFER_SIZE)
        content = pickle.loads(data)
        packets.append(content)
        packets.sort(key=lambda x: x['pos'])
    with open(fn, 'wb') as file_io:
        for packet in packets:
            file_io.write(packet['content'])


server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.settimeout(2.00)
server_socket.bind(('', SERVER_PORT))
file_prefix = os.getcwd() + "\\serverFiles\\"
print("The server is ready to receive.")
while True:
    try:
        command, client_address = server_socket.recvfrom(BUFFER_SIZE)
        command_name = command.decode().split(" ")[0]
        match command_name:
            case 'list':
                server_socket.sendto(os.listdir(file_prefix).__str__().encode(), client_address)
            case 'get':
                file_name = command.decode().split(" ")[1]
                break
            case 'put':
                file_name = command.decode().split(" ")[1]
                num = get_number_of_packets()
                sleep(1)
                receive_file(file_prefix + file_name)
                f = open(file_prefix + file_name, "r")
                print(f.read())
            case 'quit':
                server_socket.close()
    except error:
        pass
