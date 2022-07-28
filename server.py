import os
import pickle
from socket import *
from time import sleep
from server_utils import *


def write_on_file(fn, packets):
    with open(fn, 'wb') as file_io:
        for packet in packets:
            file_io.write(packet['data'])


def receive_number_of_packets():
    while True:
        try:
            num = int(receive_message().decode())
            # acknowledges that the number of packets info has arrived and is valid
            send_acknowledge(client_address)
            return num
        except ValueError:
            # acknowledges that the number of packets info is not valid
            send_not_acknowledge(client_address)


def send_number_of_packets(number):
    num = "%s" % number
    while True:
        try:
            send_message(client_address, num)
            rps = receive_message()
            if rps.decode() == 'ACK':
                break
        except error:
            pass


def receive_file(fn, num):
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
            send_acknowledge(client_address)
            break
        else:
            failed_attempts += 1
            if failed_attempts < MAX_FAILED_ATTEMPTS:
                packets.clear()
                send_retry_acknowledge(client_address)
            else:
                send_not_acknowledge(client_address)
    # writes gathered data onto the new file of name 'fn'
    write_on_file(fn, packets)


def create_packet_list(file_path):
    with open(file_path, 'rb') as file_io:
        # calculates the number of packets using the size of both the file and the buffer (considering packets' headers)
        num_of_packages = os.path.getsize(file_path) // UPLOAD_SIZE + 1
        packet_list = []
        for i in range(num_of_packages):
            msg = file_io.read(UPLOAD_SIZE)
            # each packet consists of a position and some data read from the file
            packet_list.append({'pos': i, 'data': msg})
        return packet_list


def send_packets(packet_list):
    # each packet must be sent to the client
    for packet in packet_list:
        server_socket.sendto(pickle.dumps(packet), client_address)
        sleep(0.1)


def send_file(file_path):
    # creates a list of packets by reading the file to send
    packet_list = create_packet_list(file_path)
    send_number_of_packets(packet_list.__len__())
    send_packets(packet_list)
    # waits for the acknowledgment
    while True:
        try:
            # gets the response of the client upon the arrival of the packets
            rps = receive_message()
            if rps.decode() == 'ACK':
                # this operation has been successful, therefore it is over
                break
            elif rps.decode() == 'RETRY':
                # this operation has not been successful, the client asks the server to retry
                send_packets(packet_list)
            elif rps.decode() == 'NACK':
                # this operation has not been successful, the client concludes that the operation is definitively over
                print('File transfer failed')
                break
        except error:
            # timeout error on the arrival of the acknowledgment, the server retries to obtain it
            pass


server_socket = socket(AF_INET, SOCK_DGRAM)
set_utils_socket(server_socket)
server_socket.bind(('', SERVER_PORT))
server_socket.settimeout(None)
file_prefix = os.getcwd() + "\\serverFiles\\"
print("The server is ready to receive.")

while True:
    try:
        server_socket.settimeout(None)
        command, client_address = server_socket.recvfrom(BUFFER_SIZE)
        match command.decode():
            case 'list':
                send_message(client_address, os.listdir(file_prefix).__str__().encode())
            case 'get':
                # the server has to send the file and wait for acknowledgment from the client
                server_socket.settimeout(TIMEOUT)
                file_name = receive_message().decode()
                # the server has to notify the client on the presence of the requested file among the server files
                if os.listdir(file_prefix).__contains__(file_name):
                    send_message(client_address, 'ACK')
                else:
                    send_message(client_address, 'NACK')
            case 'put':
                # the server has to collect the packets sent by the client and acknowledge the latter on the completion
                server_socket.settimeout(None)
                while True:
                    # obtains the file name and requests a check to the client on its validity
                    file_name = receive_message().decode()
                    send_message(client_address, file_name)
                    server_socket.settimeout(TIMEOUT)
                    try:
                        response = receive_message().decode()
                        # if the check is successful the name is definitively obtained
                        if response == 'ACK':
                            server_socket.settimeout(None)
                            receive_file(file_prefix + file_name, receive_number_of_packets())
                            break
                        # if the client declares the operation is unsuccessful, the connection is interrupted
                        elif response == 'NACK':
                            print('Connection failed')
                            break
                    except error:
                        # timeout error, the client has to re-send the information
                        pass
            case 'quit':
                server_socket.close()
    except error:
        pass
