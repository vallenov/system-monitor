import logging
import os
import time
import threading

from monitor import Monitor
from ini_service import load_config, ini_save
from send_service import send_message, send_confirmation_message
from cron import cron
from helpers import datetime_dict
import config


class Checker:

    block_message = {
        'ssh': {},
        'used_space': {}
    }

    unverified_ssh_connections = {}

    @staticmethod
    @cron(rule=config.CronTab.check_temperature)
    def check_temperature(**kwargs):
        """
        Проверка превышения заданной температуры
        """
        ini_conf = load_config()
        max_temp = int(ini_conf.get('MAX_VALUES', 'max_temp'))

        temp = Monitor.get_temperature()
        if temp >= max_temp and Checker.block_message.get('temperature', False) is False:
            data = dict()
            data['to'] = config.TELEGRAM_CHAT_ID
            name = Monitor.get_name_of_machine()
            data['text'] = f'Температура {name} сейчас: {temp}°C'
            send_message(data)
            logging.info('Send successful')
            Checker.block_message['temperature'] = True
        elif temp < max_temp:
            Checker.block_message['temperature'] = False

    @staticmethod
    @cron()
    def check_ssh_connections(**kwargs):
        """
        Проверка ssh соединений
        """
        connections = Monitor.get_ssh_connections()
        for conn in Checker.block_message['ssh'].keys():
            if conn not in connections:
                data = dict()
                data['to'] = config.TELEGRAM_CHAT_ID
                data['text'] = str(f'Сессия {conn} завершена.'
                                   f'Текущее количество подключений: {len(connections)}')
                send_message(data)
                Checker.block_message['ssh'].pop(conn)
        for conn in connections:
            if Checker.block_message.get('ssh', {}).get(conn, False) is False:
                data = dict()
                data['to'] = config.TELEGRAM_CHAT_ID
                name = Monitor.get_name_of_machine()
                data['text'] = str(f'Новое подключение к "{name}" с адреса {conn}.'
                                   f'Текущее количество подключений: {len(connections)}')
                send_message(data)
                Checker.block_message['ssh'][conn] = True
                if '127.0.0.1' in conn:
                    Checker.unverified_ssh_connections[conn] = 10
                    send_confirmation_message()
            elif len(connections) == 0:
                Checker.block_message['ssh'].clear()
        for conn in Checker.unverified_ssh_connections:
            Checker.unverified_ssh_connections[conn] -= 1
            if Checker.unverified_ssh_connections[conn] == 0:
                os.system('systemctl restart ngrok.service')
                send_message({
                    'to': config.TELEGRAM_CHAT_ID,
                    'text': 'Перезагрузка ngrok'
                })
                Checker.unverified_ssh_connections.clear()

    @staticmethod
    @cron(rule=config.CronTab.check_used_space)
    def check_used_space(**kwargs):
        """
        Проверка оставшегося свободного места на жестком диске
        """
        ini_conf = load_config()
        max_used_space = int(ini_conf.get('MAX_VALUES', 'max_used_space'))
        used_space = Monitor.get_used_space()
        name = Monitor.get_name_of_machine()
        for key, value in used_space.items():
            if value > max_used_space and Checker.block_message.get('used_space').get(key, False) is False:
                data = dict()
                data['to'] = config.TELEGRAM_CHAT_ID
                data['text'] = f'Свободное место в "{key}" на сервере {name} заканчивается. Осталось {100 - value}%'
                send_message(data)
                Checker.block_message['used_space'][key] = True
            elif value < max_used_space:
                Checker.block_message['used_space'][key] = False

    @staticmethod
    @cron(rule=config.CronTab.check_ip)
    def check_ip(**kwargs):
        """
        Проверка изменения IP-адреса
        """
        conf = load_config()
        old_ip = None
        if conf.has_option('SETTINGS', 'self_ip'):
            old_ip = conf.get('SETTINGS', 'self_ip')
        new_ip = Monitor.get_self_ip()
        if old_ip != new_ip or old_ip is None:
            conf.set('SETTINGS', 'self_ip', new_ip)
            ini_save(conf)
        else:
            if new_ip == old_ip:
                return
        name = Monitor.get_name_of_machine()
        data = dict()
        data['to'] = config.TELEGRAM_CHAT_ID
        data['text'] = f'Новый IP-адрес {name}: {new_ip}'
        send_message(data)

    @staticmethod
    def check_loop():
        """
        Главный цикл проверки
        """
        while True:
            try:
                now_dict = datetime_dict()
                Checker.check_ip(now_dict=now_dict)
                Checker.check_temperature(now_dict=now_dict)
                Checker.check_ssh_connections(now_dict=now_dict)
                Checker.check_used_space(now_dict=now_dict)
            except Exception as _ex:
                logging.exception(f'Unrecognized exception {_ex}')
            time.sleep(1)

    @staticmethod
    def run():
        # хинт, что бы процессы не двоились
        if 'WERKZEUG_RUN_MAIN' not in os.environ:
            cl = threading.Thread(target=Checker.check_loop)
            cl.start()
