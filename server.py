import os
import pickle
from socket import *
from time import sleep
from settings import *


def get_number_of_packets():
    while True:
        try:
            data = server_socket.recv(BUFFER_SIZE)
            # acknowledges that the number of packets info has arrived
            server_socket.sendto('ACK'.encode(), client_address)
            if data:
                n = int(data.decode())
                return n
        except error:
            pass


def write_on_file(fn, packets):
    with open(fn, 'wb') as file_io:
        for packet in packets:
            file_io.write(packet['data'])


def receive_file(fn):
    # list of packets
    packets = []
    # tries to collect packets until the number of collected packets is equal to the original number of packets
    while True:
        for i in range(num):
            data = server_socket.recv(BUFFER_SIZE)
            content = pickle.loads(data)
            packets.append(content)
            # re-orders the list based on the initial position of the packets
            packets.sort(key=lambda x: x['pos'])
        # if all packets have arrived, then the server notifies the client and proceeds to write onto the new file
        if packets.__len__() == num:
            server_socket.sendto('ACK'.encode(), client_address)
            break
        else:
            packets.clear()
            server_socket.sendto('NACK'.encode(), client_address)
    # writes gathered data onto the new file of name 'fn'
    write_on_file(fn, packets)


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
