from urllib import request

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def init():  # put application's code here
    return render_template('index.html')


@app.route('/upload-image/<url>', methods=['GET', 'POST'])
def uploadFile(url):  # put application's code here
    return url


if __name__ == '__main__':
    app.run(debug=True)
