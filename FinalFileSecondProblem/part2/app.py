from crypt import methods
import os
from turtle import st

from flask import Flask
import requests
import json
import socket


app = Flask(__name__)
data = {}

@app.route('/', methods=['GET'])
def get_datatime():
    url = data['host']
    resp = requests.get(url)
    host_name = socket.gethostname()
    out = {'hostname' : host_name , 'time' : str(resp.content)}
    json_dump = json.dumps(out)
    return json_dump



if __name__ == '__main__':
    if os.path.exists('./config/config.json'):
        with open('./config/config.json') as js_config_file:
            data = json.load(js_config_file)
    else:
        data['port'] = 8080
        data['host'] = 'http://worldtimeapi.org/api/timezone/Asia/Tehran'

    app.run(host="0.0.0.0" , debug=True , port=data['port'])