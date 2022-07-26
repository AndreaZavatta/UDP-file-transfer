from socket import *


def send_message(msg):
    clientSocket.sendto(msg.encode(), (serverName, serverPort))


def send_file(file_name):
    f = open(file_name, 'rb')
    clientSocket.sendto(f, (serverName, serverPort))
    f.close()


serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
file_prefix = 'files/'
while True:
    message = input('Input a command between list, get, put or quit to exit: ')
    match message:
        case 'list':
            send_message('list')
            file_list = clientSocket.recv(1024)
            print(file_list.decode())
        case 'get':
            send_message('get')
            filename = input('Input the filename: ')
            send_message(filename)
        case 'put':
            send_message('put')
            filename = input('Input the filename: ')
            send_file(file_prefix + filename)
        case 'quit':
            break
clientSocket.close()
