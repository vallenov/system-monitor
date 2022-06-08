from flask import Flask
import os

app = Flask(__name__)


@app.route('/start_ngrok', methods=['GET'])
def restart_ngrok():
    os.system('systemctl start ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok запущен'
    }
    return res


@app.route('/restart_ngrok', methods=['GET'])
def restart_ngrok():
    os.system('systemctl restart ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok перезапущен'
    }
    return res


@app.route('/stop_ngrok', methods=['GET'])
def restart_ngrok():
    os.system('systemctl stop ngrok.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok остановлен'
    }
    return res
