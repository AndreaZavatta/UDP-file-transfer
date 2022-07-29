import os
import pickle
from socket import *
from time import sleep
from client_utils import *
from settings import *

# initializes the client socket and client utils
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(None)
set_utils_socket(client_socket)
file_prefix = os.getcwd() + "\\clientFiles\\"


def get_client_files():
	return str(os.listdir(file_prefix))


def write_on_file(fn, packets):
	with open(fn, 'wb') as file_io:
		for packet in packets:
			file_io.write(packet['data'])


def receive_number_of_packets():
	while True:
		try:
			num = int(receive_message().decode())
			# acknowledges that the number of packets info has arrived and is valid
			send_acknowledge((SERVER_NAME, SERVER_PORT))
			return num
		except ValueError:
			# acknowledges that the number of packets info is not valid
			send_not_acknowledge((SERVER_NAME, SERVER_PORT))


def receive_file(fn, num):
	# list of packets
	packets = []
	# tries to collect packets until the number of collected packets is equal to the original number of packets
	while True:
		failed_attempts = 0
		for i in range(num):
			data = receive_message()
			content = pickle.loads(data)
			packets.append(content)
		# re-orders the list based on the initial position of the packets
		packets.sort(key=lambda x: x['pos'])
		# if all packets have arrived, then the server notifies the client and proceeds to write onto the new file
		if packets.__len__() == num:
			send_acknowledge((SERVER_NAME, SERVER_PORT))
			break
		else:
			failed_attempts += 1
			if failed_attempts < MAX_FAILED_ATTEMPTS:
				packets.clear()
				send_retry_acknowledge((SERVER_NAME, SERVER_PORT))
			else:
				send_not_acknowledge((SERVER_NAME, SERVER_PORT))
				break
	# writes gathered data onto the new file of name 'fn'
	write_on_file(fn, packets)


def create_packet_list(file_path):
	with open(file_path, 'rb') as file_io:
		num_of_packages = os.path.getsize(file_path) // UPLOAD_SIZE + 1
		packet_list = []
		for i in range(num_of_packages):
			msg = file_io.read(UPLOAD_SIZE)
			packet_list.append({'pos': i, 'data': msg})
		return packet_list


def send_number_of_packets(number):
	num = "%s" % number
	while True:
		try:
			send_message((SERVER_NAME, SERVER_PORT), num)
			rps = receive_message()
			if rps.decode() == 'ACK':
				break
		except error:
			pass


def send_file(file_path):
	# creates the list of packets that must be sent to the server
	packet_list = create_packet_list(file_path)
	# sends the number of packets first and then the packets, one by one
	send_number_of_packets(packet_list.__len__())
	upload_packet_list(packet_list)
	while True:
		try:
			# gets the acknowledgment from server on the completion of the operation
			rps = receive_message()
			if rps.decode() == 'ACK':
				return SUCCESS_CODE
			elif rps.decode() == 'RETRY':
				upload_packet_list(packet_list)
			elif rps.decode() == 'NACK':
				return ERROR_CODE
		except error:
			pass


def upload_packet_list(packet_list):
	for packet in packet_list:
		client_socket.sendto(pickle.dumps(packet), (SERVER_NAME, SERVER_PORT))
		sleep(0.1)


def list_files():
	client_socket.settimeout(TIMEOUT)
	send_message((SERVER_NAME, SERVER_PORT), "list")
	timeouts = 0
	# the arrival of the list may be timed out so there needs to be a check on it
	ret = ""
	while timeouts < MAX_FAILED_ATTEMPTS:
		try:
			file_list = receive_message()
			ret = file_list.decode()
			break
		except error:
			timeouts += 1
	return ret


def get_file(file_name):
	client_socket.settimeout(TIMEOUT)
	# sends the command to the server
	send_message((SERVER_NAME, SERVER_PORT), "get")
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
				# error code
				return ERROR_CODE
			# if the server acknowledges the file name, then the client receives the file
			elif response.decode() == 'ACK':
				receive_file(file_prefix + file_name, receive_number_of_packets())
				# success code
				return SUCCESS_CODE
			# if the server retries, then the client retries to send the file name
			elif response.decode() == 'RETRY':
				failed_attempts += 1
				send_message((SERVER_NAME, SERVER_PORT), file_name)
		except error:
			failed_attempts += 1
	# if the maximum number of attempts has been reached, the error code must be returned
	return ERROR_CODE


def put_file(file_name):
	client_socket.settimeout(TIMEOUT)
	# sends the command to the server
	send_message((SERVER_NAME, SERVER_PORT), 'put')
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
					exit_status = send_file(file_prefix + file_name)
					# the exit status is needed to display the eventual failure of the operation to the user
					return exit_status
				# if the server does not acknowledge the file name,
				# then the server notifies the client and the client tries to send the file again
				elif failed_attempts < MAX_FAILED_ATTEMPTS:
					failed_attempts += 1
					send_retry_acknowledge((SERVER_NAME, SERVER_PORT))
				# if the server does not acknowledge the file name and the client has reached the maximum number
				# of failed attempts then the client notifies the server and the client exits
				else:
					send_not_acknowledge((SERVER_NAME, SERVER_PORT))
					return ERROR_CODE
			# if the server does not respond, then the client tries to receive the acknowledgement again
			except error:
				failed_attempts += 1
	else:
		return ERROR_CODE
