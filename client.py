from client_functions import *

# main loop
while True:
    # receives the input from the user
    message = input('Input a command between list, get, put or quit to exit: ')
    command = message.split(' ')[0]
    # checks if the command is valid
    match command:
        # gets the list of files from the server and prints it
        case 'list':
            print(list_files_server())
        case 'get':
            client_socket.settimeout(TIMEOUT)
            # sends the command to the server
            send_message((SERVER_NAME, SERVER_PORT), command)
            file_name = message.split(' ')[1]
            # if the file already exists, the client overwrites it
            if os.listdir(file_prefix).__contains__(file_name):
                os.remove(file_prefix + file_name)
            # sends the file name to the server
            send_message((SERVER_NAME, SERVER_PORT), file_name)
            # waits for the server to acknowledge the file name
            failed_attempts = 0
            while failed_attempts < MAX_FAILED_ATTEMPTS:
                try:
                    response = receive_message()
                    # if the server does not acknowledge the file name or if the connection timed out,
                    # then the client exits
                    if response.decode() == 'NACK':
                        print('File not present on server or connection timed out')
                        break
                    # if the server acknowledges the file name, then the client receives the file
                    elif response.decode() == 'ACK':
                        receive_file(file_prefix + file_name, receive_number_of_packets())
                        break
                    # if the server retries, then the client retries to send the file name
                    elif response.decode() == 'RETRY':
                        failed_attempts += 1
                        send_message((SERVER_NAME, SERVER_PORT), file_name)
                except error:
                    failed_attempts += 1
            if failed_attempts == MAX_FAILED_ATTEMPTS:
                print('Connection timed out while getting file')
        case 'put':
            client_socket.settimeout(TIMEOUT)
            # sends the command to the server
            send_message((SERVER_NAME, SERVER_PORT), command)
            file_name = message.split(' ')[1]
            if os.listdir(file_prefix).__contains__(file_name):
                failed_attempts = 0
                # sends the file name to the server and waits for the server to acknowledge the file name
                while True:
                    send_message((SERVER_NAME, SERVER_PORT), file_name)
                    try:
                        response = receive_message()
                        # if the server acknowledges the file name, then the file is sent
                        if response.decode() == file_name:
                            send_acknowledge((SERVER_NAME, SERVER_PORT))
                            send_file(file_prefix + file_name)
                            break
                        # if the server does not acknowledge the file name,
                        # then the server notifies the client and the client tries to send the file again
                        elif failed_attempts < MAX_FAILED_ATTEMPTS:
                            failed_attempts += 1
                            send_retry_acknowledge((SERVER_NAME, SERVER_PORT))
                        # if the server does not acknowledge the file name and the client has reached the maximum number
                        # of failed attempts then the client notifies the server and the client exits
                        else:
                            send_not_acknowledge((SERVER_NAME, SERVER_PORT))
                            print('Connection timed out while sending file')
                            break
                    # if the server does not respond, then the client tries to receive the acknowledgement again
                    except error:
                        failed_attempts += 1
            else:
                print('File not present on client')
        # if the command is quit, then the client exits
        case 'quit':
            break
        # if the command is not valid, then the client notifies the user
        case default:
            print('Invalid command')
client_socket.close()
