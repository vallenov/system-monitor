from flask import Flask
import os
from monitor import Monitor

app = Flask(__name__)


@app.route('/ngrok_start', methods=['GET'])
def start_ngrok():
    os.system('systemctl start ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok запущен'
    }
    return res


@app.route('/ngrok_restart', methods=['GET'])
def restart_ngrok():
    os.system('systemctl restart ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok перезапущен'
    }
    return res


@app.route('/ngrok_stop', methods=['GET'])
def stop_ngrok():
    os.system('systemctl stop ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok остановлен'
    }
    return res


@app.route('/ngrok_db_start', methods=['GET'])
def start_ngrok_db():
    os.system('systemctl start ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB запущен'
    }
    return res


@app.route('/ngrok_db_restart', methods=['GET'])
def restart_ngrok_db():
    os.system('systemctl restart ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB перезапущен'
    }
    return res


@app.route('/ngrok_db_stop', methods=['GET'])
def stop_ngrok_db():
    os.system('systemctl stop ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB остановлен'
    }
    return res


@app.route('/ngrok_tunnels', methods=['GET'])
def stop_ngrok_db():
    return Monitor.get_ngrok_tunnels()
