from flask import Flask
from flask_restful import request
import os
import subprocess as sp
import time

from monitor import Monitor

app = Flask(__name__)


@app.route('/ngrok_<act>', methods=['GET'])
def ngrok_ssh(action):
    os.system(f'systemctl {action} ngrok.service')
    res = {
        'res': 'OK',
        'msg': f'Ngrok {action}'
    }
    return res


@app.route('/ngrok_db_<action>', methods=['GET'])
def ngrok_db(action):
    os.system(f'systemctl {action} ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': f'Ngrok DB {action}'
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


@app.route('/system_restart', methods=['GET'])
def system_restart():
    os.system('reboot')


@app.route('/systemctl', methods=['GET'])
def systemctl():
    action = request.args.get('action', None)
    service = request.args.get('service', None)
    if not action or not service:
        return {
            'msg': 'Не найдены данные о сервисе и/или действии'
        }
    try:
        result = sp.check_output(f'systemctl {action} {service}.service', shell=True) or None
    except sp.CalledProcessError as spe:
        return {
            'msg': f'Команда "{spe.cmd}" вернула код: {spe.returncode}'
        }
    if result:
        return {
            'msg': result.decode()
        }
    return {
        'msg': f'К сервису {service} применена команда {action}'
    }


@app.route('/test', methods=['GET'])
def test():
    return {'msg': 'OK'}
