import os
from socket import *


def create_file():
    data = serverSocket.recv(1000000)
    file = open("", 'wb')
    file.write(data.strip())


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
file_prefix = "serverFiles/"
print("The server is ready to receive.")
while True:
    command, clientAddress = serverSocket.recvfrom(2048)
    commandName = command.decode().split(" ")[0]
    match commandName:
        case 'list':
            serverSocket.sendto(os.listdir(file_prefix).__str__().encode(), clientAddress)
        case 'get':
            fileName = command.decode().split(" ")[1]
            break
        case 'put':
            fileName = command.decode().split(" ")[1]
            create_file()
        case 'quit':
            serverSocket.close()
            break
