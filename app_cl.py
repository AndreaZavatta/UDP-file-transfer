from client import *


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
			res = get_file(message.split(' ')[1])
			if res == ERROR_CODE:
				print('File not present on server or connection timed out')
		case 'put':
			res = put_file(message.split(' ')[1])
			if res == ERROR_CODE:
				print('Connection timed out')
		# if the command is quit, then the client exits
		case 'quit':
			close_server()
			break
		# if the command is not valid, then the client notifies the user
		case default:
			print('Invalid command')
client_socket.close()
