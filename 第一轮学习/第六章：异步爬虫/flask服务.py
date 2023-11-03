import time
from flask import Flask

app = Flask(__name__)

@app.route('/chen')
def index_chen():
    time.sleep(2)
    return 'Hello chen'

@app.route('/jay')
def index_jay():
    time.sleep(2)
    return 'Hello jay'

@app.route('/Tom')
def index_tom():
    time.sleep(2)
    return 'Hello Tom'

if __name__ == '__main__':
    app.run(threaded=True)