from socket import *


def send_message(msg):
    clientSocket.sendto(msg.encode(), (serverName, serverPort))


serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
while True:
    message = input('Input a command between list, get, put or quit to exit: ')
    match message:
        case 'list':
            send_message('list')
        case 'get':
            filename = input('Input the filename: ')
            send_message('get ' + filename)
        case 'put':
            filename = input('Input the filename: ')
            send_message('put ' + filename)
        case 'quit':
            break
clientSocket.close()
