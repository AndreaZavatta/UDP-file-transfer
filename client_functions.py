import os
import pickle
from socket import *
from time import sleep
from client_utils import *
from settings import *


def write_on_file(fn, packets):
    with open(fn, 'wb') as file_io:
        for packet in packets:
            file_io.write(packet['data'])


def receive_number_of_packets():
    while True:
        try:
            num = int(receive_message().decode())
            # acknowledges that the number of packets info has arrived and is valid
            send_acknowledge((SERVER_NAME, SERVER_PORT))
            return num
        except ValueError:
            # acknowledges that the number of packets info is not valid
            send_not_acknowledge((SERVER_NAME, SERVER_PORT))


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
            send_acknowledge((SERVER_NAME, SERVER_PORT))
            break
        else:
            failed_attempts += 1
            if failed_attempts < MAX_FAILED_ATTEMPTS:
                packets.clear()
                send_retry_acknowledge((SERVER_NAME, SERVER_PORT))
            else:
                send_not_acknowledge((SERVER_NAME, SERVER_PORT))
                break
    # writes gathered data onto the new file of name 'fn'
    write_on_file(fn, packets)


def create_packet_list(file_path):
    with open(file_path, 'rb') as file_io:
        num_of_packages = os.path.getsize(file_path) // UPLOAD_SIZE + 1
        packet_list = []
        for i in range(num_of_packages):
            msg = file_io.read(UPLOAD_SIZE)
            packet_list.append({'pos': i, 'data': msg})
        return packet_list


def send_number_of_packets(number):
    num = "%s" % number
    while True:
        try:
            send_message((SERVER_NAME, SERVER_PORT), num)
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