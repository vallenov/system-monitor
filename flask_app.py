from flask import Flask
import os
from monitor import Monitor

app = Flask(__name__)


@app.route('/ngrok_start', methods=['GET'])
def ngrok_start():
    os.system('systemctl start ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok запущен'
    }
    return res


@app.route('/ngrok_restart', methods=['GET'])
def ngrok_restart():
    os.system('systemctl restart ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok перезапущен'
    }
    return res


@app.route('/ngrok_stop', methods=['GET'])
def ngrok_stop():
    os.system('systemctl stop ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok остановлен'
    }
    return res


@app.route('/ngrok_db_start', methods=['GET'])
def ngrok_db_start():
    os.system('systemctl start ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB запущен'
    }
    return res


@app.route('/ngrok_db_restart', methods=['GET'])
def ngrok_db_restart():
    os.system('systemctl restart ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB перезапущен'
    }
    return res


@app.route('/ngrok_db_stop', methods=['GET'])
def ngrok_db_stop():
    os.system('systemctl stop ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB остановлен'
    }
    return res


@app.route('/ngrok_tunnels', methods=['GET'])
def ngrok_tunnels():
    return Monitor.get_ngrok_tunnels()


@app.route('/ip', methods=['GET'])
def ip():
    res = {
        'ip': Monitor.get_self_ip()
    }
    return res


@app.route('/tbot_restart', methods=['GET'])
def tbot_restart():
    os.system('systemctl restart TBot.service')


@app.route('/malinka_restart', methods=['GET'])
def malinka_restart():
    os.system('reboot')
