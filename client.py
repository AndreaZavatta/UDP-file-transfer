from socket import *
from settings import *


def send_message(msg):
    client_socket.sendto(msg.encode(), (SERVER_NAME, SERVER_PORT))


def send_file(file_path):
    with open(file_path, 'rb') as file_io:
        packages = file_io.read().__len__() // BUFFER_SIZE + 1
        for i in range(packages):
            msg = file_io.read(BUFFER_SIZE)
            client_socket.sendto(msg, (SERVER_NAME, SERVER_PORT))
        client_socket.sendto(b'EOF', (SERVER_NAME, SERVER_PORT))


client_socket = socket(AF_INET, SOCK_DGRAM)
file_prefix = 'clientFiles/'
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
