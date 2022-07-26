from socket import *


def send_message(msg):
    clientSocket.sendto(msg.encode(), (serverName, serverPort))


def send_file(file_name):
    fi = open(file_name, 'rb')
    clientSocket.sendto(fi, (serverName, serverPort))
    fi.close()


serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
file_prefix = 'clientFiles/'
while True:
    message = input('Input a command between list, get, put or quit to exit: ')
    command = message.split(' ')[0]
    match command:
        case 'list':
            send_message('list')
            file_list = clientSocket.recv(1024)
            print(file_list.decode())
        case 'get':
            file_name = message.split(' ')[1]
            send_message(message)
            file = clientSocket.recv(1024)
            f = open(file_prefix + file_name, 'wb')
            f.write(file.strip())
        case 'put':
            file_name = message.split(' ')[1]
            send_message(message)
            send_file(file_prefix + file_name)
        case 'quit':
            break
clientSocket.close()
