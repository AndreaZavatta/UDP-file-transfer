import base64
import datetime
import json
from json import JSONEncoder
from flask import request
from flask import Flask, render_template
from socket import *

from client_functions import *
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


@app.route('/list/', methods=['GET'])
def fileList():
	return list_files_server()


@app.route('/get/', methods=['GET'])
def getFileList():
	filename = request.args.get('filename')
	return str(get_files(filename))


if __name__ == '__main__':
	app.run(debug=True)
