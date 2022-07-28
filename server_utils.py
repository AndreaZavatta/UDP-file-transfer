from settings import *


def send_acknowledge(server_socket, client_address):
    server_socket.sendto('ACK'.encode(), client_address)


def send_not_acknowledge(server_socket, client_address):
    server_socket.sendto('NACK'.encode(), client_address)


def send_retry_acknowledge(server_socket, client_address):
    server_socket.sendto('RETRY'.encode(), client_address)


def receive_message(server_socket):
    server_socket.recv(BUFFER_SIZE)
