
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def init():  # put application's code here
    return render_template('index.html')


@app.route('/upload-image/', methods=['GET', 'POST'])
def uploadFile():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
