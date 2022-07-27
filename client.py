import os
import pickle
from socket import *

from settings import *


def send_message(msg):
    client_socket.sendto(msg.encode(), (SERVER_NAME, SERVER_PORT))


def number_of_packets(file_path):
    with open(file_path, 'rb') as file_io:
        return file_io.read().__len__() // BUFFER_SIZE + 1


def create_packet_list(file_path):
    with open(file_path, 'rb') as file_io:
        packages = number_of_packets(file_path)
        packet_list = []
        for i in range(packages):
            msg = file_io.read(BUFFER_SIZE)
            packet_list.append({'pos': i, 'data': msg})
        return packet_list


def send_number_of_packets(number):
    while True:
        try:
            client_socket.sendto(number.__str__().encode(), (SERVER_NAME, SERVER_PORT))
            response = client_socket.recv(BUFFER_SIZE)
            if response.decode() == 'ACK':
                break
        except error:
            client_socket.sendto(number.__str__().encode(), (SERVER_NAME, SERVER_PORT))


def send_file(file_path):
    packet_list = create_packet_list(file_path)
    send_number_of_packets(number_of_packets(file_path))
    for packet in packet_list:
        client_socket.sendto(pickle.dumps(packet), (SERVER_NAME, SERVER_PORT))


client_socket = socket(AF_INET, SOCK_DGRAM)
file_prefix = os.getcwd() + "\\clientFiles\\"
while True:
    message = input('Input a command between list, get, put or quit to exit: ')
    command = message.split(' ')[0]
    match command:
        case 'list':
            send_message('list')
            file_list = client_socket.recv(BUFFER_SIZE)
            print(file_list.decode())
        case 'get':
            file_name = message.split(' ')[1]
            send_message(message)
            file = client_socket.recv(BUFFER_SIZE)
            f = open(file_prefix + file_name, 'wb')
            f.write(file.strip())
            f.close()
        case 'put':
            file_name = message.split(' ')[1]
            send_message(message)
            send_file(file_prefix + file_name)
        case 'quit':
            break
        case default:
            print('Invalid command')
client_socket.close()
