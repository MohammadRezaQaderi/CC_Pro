import os
from flask import Flask
import socket
import json
import requests

app = Flask(__name__)

configs = None


# this handle the get request
@app.route('/time', methods=['GET'])
def time_world():
    time_api = configs['address']
    time = requests.get(time_api)
    response = {'host_name': socket.gethostname(),
                'time': str(time.content)}
    final_json = json.dumps(response)
    return final_json



if __name__ == '__main__':
    if(os.path.isfile('./config-cluster.json')):
        with open('config.json') as conf:
            configs = json.load(conf)
    else:
        with open('config.json') as conf:
            configs = json.load(conf)
    app.run(host='0.0.0.0', debug=True, port=configs['port'])
