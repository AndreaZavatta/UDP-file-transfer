import os
import pickle
from settings import *
from socket import *


def receive_file(fn):
    number_of_packets = 1
    with open(fn, 'wb') as file_io:
        for i in range(number_of_packets):
            data = server_socket.recv(BUFFER_SIZE)
            content = pickle.loads(data)
            file_io.write(content)


server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', SERVER_PORT))
file_prefix = os.getcwd() + "\\serverFiles\\"
print("The server is ready to receive.")
while True:
    command, client_address = server_socket.recvfrom(2048)
    command_name = command.decode().split(" ")[0]
    match command_name:
        case 'list':
            server_socket.sendto(os.listdir(file_prefix).__str__().encode(), client_address)
        case 'get':
            file_name = command.decode().split(" ")[1]
            break
        case 'put':
            file_name = command.decode().split(" ")[1]
            receive_file(file_prefix + file_name)
            f = open(file_prefix + file_name, "r")
            print(f.read())
        case 'quit':
            server_socket.close()
