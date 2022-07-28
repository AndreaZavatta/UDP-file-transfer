from socket import socket
from settings import *


def set_utils_socket(sck: socket):
    global server_socket
    server_socket = sck


def send_acknowledge(client_address):
    server_socket.sendto('ACK'.encode(), client_address)


def send_not_acknowledge(client_address):
    server_socket.sendto('NACK'.encode(), client_address)


def send_retry_acknowledge(client_address):
    server_socket.sendto('RETRY'.encode(), client_address)


def receive_message():
    return server_socket.recv(BUFFER_SIZE)


def send_message(client_address, message: (str, int)):
    server_socket.sendto(message.encode(), client_address)


server_socket: socket
