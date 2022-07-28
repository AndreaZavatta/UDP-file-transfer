import base64
import datetime
import json
from json import JSONEncoder
from flask import request

from flask import Flask, render_template

app = Flask(__name__)


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class File:
    def __init__(self, name, dimension, data):
        self.name = name
        self.dimension = dimension
        self.data = data


@app.route('/')
def init():
    return render_template('index.html')


@app.route('/upload-file/', methods=['GET', 'POST'])
def uploadFile():
    # contenuto = base64 del file
    contenuto = request.form.get('contenuto')
    # message_byte = byte array del file
    message_bytes = base64.b64decode(contenuto)
    nomefile = request.form.get('nomefile')
    list.append(File(nomefile, len(message_bytes), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    return "0"


list = [File("firstFile", 3, "9 hours ago"), File("secondFile", 4, "10 mins ago"), File("thirdFile", 27, "11 days ago")]


@app.route('/getFileList/', methods=['GET'])
def getFileList():
    return MyEncoder().encode(list)


if __name__ == '__main__':
    app.run(debug=True)
