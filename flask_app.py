from flask_restful import request
import os
import subprocess as sp

from monitor import Monitor
import services.check_metrics as sc
from app import app


@app.route('/ngrok_<action>', methods=['GET'])
def ngrok_ssh(action):
    """
    Управление сервисами ngrok
    """
    os.system(f'systemctl {action} ngrok.service')
    res = {
        'res': 'OK',
        'msg': f'Ngrok {action}'
    }
    return res


@app.route('/serveo_ssh_<action>', methods=['GET'])
def serveo_ssh(action):
    """
    Управление сервисами serveo
    """
    os.system(f'systemctl {action} serveo_ssh.service')
    res = {
        'res': 'OK',
        'msg': f'Serveo {action}'
    }
    return res


@app.route('/ngrok_db_<action>', methods=['GET'])
def ngrok_db(action):
    """
    Управление сервисами ngrok_db
    """
    os.system(f'systemctl {action} ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': f'Ngrok DB {action}'
    }
    return res


@app.route('/ngrok_tunnels', methods=['GET'])
def ngrok_tunnels():
    return {'msg': Monitor.get_ngrok_tunnels()}


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


@app.route('/system_info', methods=['GET'])
def system_info():
    server_name = Monitor.get_name_of_machine()
    server_temperature = Monitor.get_temperature()
    server_used_space = Monitor.get_used_space()
    server_ip = Monitor.get_self_ip()
    server_ssh_connections = Monitor.get_ssh_connections()
    server_ngrok_tunnels = Monitor.get_ngrok_tunnels()
    server_uptime = Monitor.uptime()
    res = {
        'Name': server_name,
        'Temp': server_temperature,
        'Disk': server_used_space,
        'IP': server_ip,
        'SSH connections': server_ssh_connections,
        'Ngrok tunnels': server_ngrok_tunnels,
        'Uptime': server_uptime
    }
    return {'msg': res}


@app.route('/test', methods=['GET'])
def test():
    return {'msg': 'OK'}


@app.route('/allow_connection', methods=['GET'])
def allow_connection():
    sc.Checker.unverified_ssh_connections.clear()
    return {
        'msg': 'Соединение подтверждено'
    }
