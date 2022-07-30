import atexit
import subprocess
from json import JSONEncoder
from flask import request
from flask import Flask, render_template
from client import *

app = Flask(__name__)


class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__


@app.route('/')
def init():
	return render_template('index.html')


@app.route('/list/', methods=['GET'])
def files_server():
	return list_files()


@app.route('/get/', methods=['GET'])
def download():
	filename = request.args.get('filename')
	return str(get_file(filename))


@app.route('/put/', methods=['GET'])
def upload():
	filename = request.args.get('filename')
	a = put_file(filename)
	return str(a)


@app.route('/getclient/', methods=['GET'])
def files_client():
	return get_client_files()


if __name__ == '__main__':
	p = subprocess.Popen(['python', 'server.py'])
	atexit.register(lambda: p.kill())
	app.run(debug=False)
