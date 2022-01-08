from flask import Flask, request, render_template
import queue
import ast

from config import PORT

app = Flask(__name__)

data_queue = dict()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/tv", methods=['POST'])
def alert():

    data = request.get_data(as_text=True)

    data = ast.literal_eval(data)
    if not isinstance(data, dict):
        print('Warning Invalid Signal Received')

        return 'Bad Request', 400

    else:
        # Check if the key has a queue, if not, make the key.
        if data['symbol'] not in data_queue.keys():
            data_queue[data['symbol']] = []

        try:
            data_queue[data['symbol']].append(data)

        except KeyError as e:
            print("WARNING: Data Received not in the correct format. Missing Key: {}".format(e))
            return 'Bad Request', 400


        return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
