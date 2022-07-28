from socket import socket
from settings import *


def set_utils_socket(sck: socket):
    global client_socket
    client_socket = sck


def send_acknowledge(server_address):
    client_socket.sendto('ACK'.encode(), server_address)


def send_not_acknowledge(server_address):
    client_socket.sendto('NACK'.encode(), server_address)


def send_retry_acknowledge(server_address):
    client_socket.sendto('RETRY'.encode(), server_address)


def receive_message():
    return client_socket.recv(BUFFER_SIZE)


def send_message(server_address, message: (str, int)):
    client_socket.sendto(message.encode(), server_address)


client_socket: socket
