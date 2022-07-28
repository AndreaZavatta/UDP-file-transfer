import os
import pickle
from socket import *
from time import sleep

from settings import *


def send_message(msg):
    client_socket.sendto(msg.encode(), (SERVER_NAME, SERVER_PORT))


def receive_message():
    return client_socket.recv(BUFFER_SIZE)


def write_on_file(fn, packets):
    with open(fn, 'wb') as file_io:
        for packet in packets:
            file_io.write(packet['data'])


def receive_number_of_packets():
    while True:
        try:
            data = receive_message()
            # acknowledges that the number of packets info has arrived
            send_message('ACK')
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
            data = receive_message()
            content = pickle.loads(data)
            packets.append(content)
            print('Received packet %s' % content['pos'])
        # re-orders the list based on the initial position of the packets
        packets.sort(key=lambda x: x['pos'])
        # if all packets have arrived, then the server notifies the client and proceeds to write onto the new file
        if packets.__len__() == num:
            send_message('ACK')
            break
        else:
            failed_attempts += 1
            if failed_attempts < MAX_FAILED_ATTEMPTS:
                packets.clear()
                send_message('RETRY')
            else:
                send_message('NACK')
                break
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
            send_message(num)
            rps = receive_message()
            if rps.decode() == 'ACK':
                break
        except error:
            pass


def send_file(file_path):
    packet_list = create_packet_list(file_path)
    send_number_of_packets(packet_list.__len__())
    upload_packet_list(packet_list)
    while True:
        try:
            rps = receive_message()
            if rps.decode() == 'ACK':
                break
            elif rps.decode() == 'RETRY':
                upload_packet_list(packet_list)
            elif rps.decode() == 'NACK':
                print('File transfer failed')
                break
        except error:
            pass


def upload_packet_list(packet_list):
    for packet in packet_list:
        client_socket.sendto(pickle.dumps(packet), (SERVER_NAME, SERVER_PORT))
        sleep(0.1)


client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(None)
file_prefix = os.getcwd() + "\\clientFiles\\"
while True:
    message = input('Input a command between list, get, put or quit to exit: ')
    command = message.split(' ')[0]
    match command:
        case 'list':
            send_message(command)
            file_list = receive_message()
            print(file_list.decode())
        case 'get':
            client_socket.settimeout(None)
            file_name = message.split(' ')[1]
            send_message(command)
            send_message(file_name)
            response = receive_message()
            if response.decode() == 'NACK':
                print('File not present on server')
            elif response.decode() == 'ACK':
                receive_file(file_prefix + file_name, receive_number_of_packets())
        case 'put':
            client_socket.settimeout(2)
            file_name = message.split(' ')[1]
            send_message(command)
            send_message(file_name)
            send_file(file_prefix + file_name)
        case 'quit':
            break
        case default:
            print('Invalid command')
client_socket.close()
