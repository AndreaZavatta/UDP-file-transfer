import base64

from flask import request

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def init():
    return render_template('index.html')


@app.route('/upload-image/', methods=['GET', 'POST'])
def uploadFile():
    ret = 0
    try:
        # contenuto = base64 del file
        contenuto = request.form.get('contenuto')
        # message_byte = byte array del file
        message_bytes = base64.b64decode(contenuto)
        nomefile = request.form.get('nomefile')
    except:
        ret = 1

    return str(ret)


if __name__ == '__main__':
    app.run(debug=True)
