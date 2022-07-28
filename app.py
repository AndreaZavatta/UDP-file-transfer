import base64
import json
from json import JSONEncoder
from flask import request

from flask import Flask, render_template

app = Flask(__name__)


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class File:
    def __init__(self, name, dimension):
        self.name = name
        self.dimension = dimension


@app.route('/')
def init():
    return render_template('index.html')


@app.route('/upload-file/', methods=['GET', 'POST'])
def uploadFile():
    ret = 0
    try:
        # contenuto = base64 del file
        contenuto = request.form.get('contenuto')
        # message_byte = byte array del file
        message_bytes = base64.b64decode(contenuto)
        nomefile = request.form.get('nomefile')
        list.append(File(nomefile, 3))
    except:
        ret = 1
    return str(ret)


list = [File("firstFile", 3), File("secondFile", 4), File("thirdFile", 27)]


@app.route('/getFileList/', methods=['GET'])
def getFileList():
    return MyEncoder().encode(list)


if __name__ == '__main__':
    app.run(debug=True)
