from socket import *


def create_file():
    data = serverSocket.recv(1000000)
    file = open("", 'wb')
    file.write(data.strip())


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive. Fuck you nigga")
while True:
    command, clientAddress = serverSocket.recvfrom(2048)
    commandName, fileName = command.decode().split(" ")
    match commandName:
        case 'list':
            break
        case 'get':
            break
        case 'put':
            create_file()
        case 'quit':
            serverSocket.close()
            break
