import base64
import datetime
import json
from json import JSONEncoder
from flask import request
from flask import Flask, render_template
from socket import *

from client_utils import send_message, receive_message, set_utils_socket
from settings import *

app = Flask(__name__)


class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__


@app.route('/')
def init():
	return render_template('index.html')


@app.route('/upload-file/', methods=['GET', 'POST'])
def uploadFile():
	"""contenuto = base64 del file
    contenuto = request.form.get('contenuto')
    message_byte = byte array del file
    message_bytes = base64.b64decode(contenuto)
    nomefile = request.form.get('nomefile')
    list.append(File(nomefile, len(message_bytes), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    """
	nomefile = request.form.get('nomefile')








	# upload_file(nomefile)
	return "0"


@app.route('/getFileList/', methods=['GET'])
def getFileList():
	client_socket = socket(AF_INET, SOCK_DGRAM)
	client_socket.settimeout(TIMEOUT)
	set_utils_socket(client_socket)
	send_message((SERVER_NAME, SERVER_PORT), 'list')
	file_list = receive_message()
	ret = file_list.decode()
	#jsonRet = json.loads(ret)
	client_socket.close()
	return ret


if __name__ == '__main__':
	app.run(debug=True)
