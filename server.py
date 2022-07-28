import os
import pickle
from socket import *
from time import sleep
from settings import *


def write_on_file(fn, packets):
    with open(fn, 'wb') as file_io:
        for packet in packets:
            file_io.write(packet['data'])


def receive_number_of_packets():
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


def receive_file(fn, num):
    # list of packets
    packets = []
    # tries to collect packets until the number of collected packets is equal to the original number of packets
    while True:
        failed_attempts = 0
        print(num)
        for i in range(num):
            data = server_socket.recv(BUFFER_SIZE)
            content = pickle.loads(data)
            packets.append(content)
            print('Received packet %s' % content['pos'])
        # re-orders the list based on the initial position of the packets
        packets.sort(key=lambda x: x['pos'])
        # if all packets have arrived, then the server notifies the client and proceeds to write onto the new file
        if packets.__len__() == num:
            server_socket.sendto('ACK'.encode(), client_address)
            break
        else:
            failed_attempts += 1
            if failed_attempts < MAX_FAILED_ATTEMPTS:
                packets.clear()
                server_socket.sendto('RETRY'.encode(), client_address)
            else:
                server_socket.sendto('NACK'.encode(), client_address)
    # writes gathered data onto the new file of name 'fn'
    write_on_file(fn, packets)


def create_packet_list(file_path):
    with open(file_path, 'rb') as file_io:
        num_of_packages = file_io.read().__len__() // UPLOAD_SIZE + 1
        packet_list = []
        for i in range(num_of_packages):
            msg = file_io.read(UPLOAD_SIZE)
            packet_list.append({'pos': i, 'data': msg})
        return packet_list


def send_number_of_packets(number):
    num = "%s" % number
    while True:
        try:
            server_socket.sendto(num.encode(), client_address)
            rps = server_socket.recv(BUFFER_SIZE)
            if rps.decode() == 'ACK':
                break
        except error:
            pass


def upload_packet_list(packet_list):
    for packet in packet_list:
        server_socket.sendto(pickle.dumps(packet), client_address)
        sleep(0.1)


def send_file(file_path):
    packet_list = create_packet_list(file_path)
    send_number_of_packets(packet_list.__len__())
    upload_packet_list(packet_list)
    while True:
        try:
            rps = server_socket.recv(BUFFER_SIZE)
            if rps.decode() == 'ACK':
                break
            elif rps.decode() == 'RETRY':
                upload_packet_list(packet_list)
            elif rps.decode() == 'NACK':
                print('File transfer failed')
                break
        except error:
            pass


server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.settimeout(None)
server_socket.bind(('', SERVER_PORT))
file_prefix = os.getcwd() + "\\serverFiles\\"
print("The server is ready to receive.")
while True:
    try:
        command, client_address = server_socket.recvfrom(BUFFER_SIZE)
        match command.decode():
            case 'list':
                server_socket.sendto(os.listdir(file_prefix).__str__().encode(), client_address)
            case 'get':
                file_name = server_socket.recv(BUFFER_SIZE).decode()
                if os.listdir(file_prefix).__contains__(file_name):
                    server_socket.sendto('ACK'.encode(), client_address)
                else:
                    server_socket.sendto('NACK'.encode(), client_address)
            case 'put':
                file_name = server_socket.recv(BUFFER_SIZE).decode()
                receive_file(file_prefix + file_name, receive_number_of_packets())
            case 'quit':
                server_socket.close()
    except error:
        pass
