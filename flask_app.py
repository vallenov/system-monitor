from flask import Flask
import os

app = Flask(__name__)


@app.route('/restart_ngrok', methods=['GET'])
def restart_ngrok():
    os.system('systemctl restart ngrok.service')
    return {'res': 'OK'}
