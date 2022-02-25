from flask import Flask, request, jsonify, redirect
import pymysql
import shortuuid
from datetime import datetime, timedelta
import json
import os


if os.path.exists("./config.json"):
    host_secret = os.environ.get("HOST_TOKEN")
    pass_secret = os.environ.get("PASS_TOKEN")
    with open("./config.json") as json_config_file:
        data = json.load(json_config_file)
        if "port" not in data.keys() or "exp" not in data.keys() or "host" not in data.keys() or "password" not in data.keys() or "db" not in data.keys():
            f = open("secret.json")
            data = json.load(f)
else:
    with open("secret.json") as json_config_file:
        data = json.load(json_config_file)
        host_secret = data['host']
        pass_secret = data['password']

            


serverPort = data['port']
expDuration = data['exp']
dbHost = host_secret
dbPassword = pass_secret
dbName = data['db']
dbPort = data['sql_port']

application = app = Flask(__name__)


def get_connection():
    connection = pymysql.connect(host=dbHost, user="root", password=dbPassword,
                                 db=dbName, port=dbPort, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection


@app.route('/shorten', methods=["POST"])
def shorten():
    if request and request.json['link']:
        link = request.json['link']
        con = get_connection()
        cur = con.cursor()
        short_url = shortuuid.ShortUUID().random(length=7)
        query = "INSERT INTO urls (link, short_url) VALUES (%s, %s)"
        cur.execute(query, (link, short_url))
        con.commit()
        cur.close()
        con.close()
        return jsonify({"short_url": short_url})
    return jsonify({"error": "Please proive an URL to shorten."})


@app.route('/<short_url>')
def getlink(short_url):
    con = get_connection()
    cur = con.cursor()
    query = "SELECT * FROM urls WHERE short_url = %s"
    cur.execute(query, (short_url))
    data = cur.fetchone()
    if data:
        now = datetime.now()
        start = data['start_time']
        exp = start + timedelta(minutes=expDuration)
        if(now > exp):
            con = get_connection()
            cur = con.cursor()
            query = "DELETE FROM urls WHERE short_url = %s"
            cur.execute(query, (short_url))
            con.commit()
            return jsonify({"error": " Not found"})
        else:
            return redirect(data['link'])

    cur.close()
    con.close()
    return jsonify({"error": "No data found"})


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=serverPort, debug=True)