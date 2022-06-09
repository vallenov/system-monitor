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


@app.route('/start_ngrok_db', methods=['GET'])
def restart_ngrok_db():
    os.system('systemctl start ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB запущен'
    }
    return res


@app.route('/restart_ngrok_db', methods=['GET'])
def restart_ngrok_db():
    os.system('systemctl restart ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB перезапущен'
    }
    return res


@app.route('/stop_ngrok_db', methods=['GET'])
def restart_ngrok_db():
    os.system('systemctl stop ngrok_db.service')
    res = {
        'res': 'OK',
        'msg': 'Ngrok DB остановлен'
    }
    return res
