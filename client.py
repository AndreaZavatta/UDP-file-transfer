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
			print(list_files())
		case 'get':
			file = get_file(message.split(' ')[1])
			if file == ERROR_CODE:
				print('File not present on server or connection timed out')
			else:
				print('Connection timed out while getting file')
		case 'put':
			put_file(message.split(' ')[1])
		# if the command is quit, then the client exits
		case 'quit':
			break
		# if the command is not valid, then the client notifies the user
		case default:
			print('Invalid command')
client_socket.close()