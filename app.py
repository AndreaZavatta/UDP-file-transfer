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


@app.route('/list/', methods=['GET'])
def file_list():
	return list_files_server()


@app.route('/get/', methods=['GET'])
def get_file_list():
	filename = request.args.get('filename')
	return str(get_files(filename))


@app.route('/put/', methods=['GET'])
def putFile():
	filename = request.args.get('filename')
	a = put_file(filename)
	return str(a)


if __name__ == '__main__':
	app.run(debug=True)
