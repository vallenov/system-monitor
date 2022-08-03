import logging
import os
import time
import threading

from monitor import Monitor
from ini_service import load_config, ini_save
from send_service import send_message, send_confirmation_message


class Checker:

    block_message = {
        'ssh': {},
        'used_space': {}
    }

    unverified_ssh_connections = {}

    @staticmethod
    def check_temperature():
        """
        Проверка превышения заданной температуры
        """
        conf = load_config()
        max_temp = int(conf.get('MAX_VALUES', 'max_temp'))

        temp = Monitor.get_temperature()
        if temp >= max_temp and Checker.block_message.get('temperature', False) is False:
            data = dict()
            data['to'] = int(conf.get('CONTACT', 'telegram_chat_id'))
            name = Monitor.get_name_of_machine()
            data['text'] = f'Температура {name} сейчас: {temp}°C'
            send_message(data)
            logging.info('Send successful')
            Checker.block_message['temperature'] = True
        elif temp < max_temp:
            Checker.block_message['temperature'] = False

    @staticmethod
    def check_ssh_connections():
        """
        Проверка ssh соединений
        """
        conf = load_config()
        connections = Monitor.get_ssh_connections()
        for conn in Checker.block_message['ssh'].keys():
            if conn not in connections:
                data = dict()
                data['to'] = int(conf.get('CONTACT', 'telegram_chat_id'))
                data['text'] = str(f'Сессия {conn} завершена.'
                                   f'Текущее количество подключений: {len(connections)}')
                send_message(data)
                Checker.block_message['ssh'].pop(conn)
        for conn in connections:
            if Checker.block_message.get('ssh', {}).get(conn, False) is False:
                data = dict()
                data['to'] = int(conf.get('CONTACT', 'telegram_chat_id'))
                name = Monitor.get_name_of_machine()
                data['text'] = str(f'Новое подключение к "{name}" с адреса {conn}.'
                                   f'Текущее количество подключений: {len(connections)}')
                send_message(data)
                Checker.block_message['ssh'][conn] = True
                if conn.startswith('127.0.0.1'):
                    Checker.unverified_ssh_connections[conn] = 10
                    send_confirmation_message()
            elif len(connections) == 0:
                Checker.block_message['ssh'].clear()
        for conn in Checker.unverified_ssh_connections:
            Checker.unverified_ssh_connections[conn] -= 1
            if Checker.unverified_ssh_connections[conn] == 0:
                os.system('systemctl restart ngrok.service')
                send_message({
                    'to': conf.get('TELEBOT', 'root_id'),
                    'text': 'Перезагрузка ngrok'
                })
                Checker.unverified_ssh_connections.clear()

    @staticmethod
    def check_used_space():
        """
        Проверка оставшегося свободного места на жестком диске
        """
        conf = load_config()
        max_used_space = int(conf.get('MAX_VALUES', 'max_used_space'))
        used_space = Monitor.get_used_space()
        name = Monitor.get_name_of_machine()
        for key, value in used_space.items():
            if value > max_used_space and Checker.block_message.get('used_space').get(key, False) is False:
                data = dict()
                data['to'] = int(conf.get('CONTACT', 'telegram_chat_id'))
                data['text'] = f'Свободное место в "{key}" на сервере {name} заканчивается. Осталось {100 - value}%'
                send_message(data)
                Checker.block_message['used_space'][key] = True
            elif value < max_used_space:
                Checker.block_message['used_space'][key] = False

    @staticmethod
    def check_ip():
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
        data['to'] = int(conf.get('CONTACT', 'telegram_chat_id'))
        data['text'] = f'Новый IP-адрес {name}: {new_ip}'
        send_message(data)

    @staticmethod
    def check_loop():
        """
        Главный цикл проверки
        """
        i = 0
        sec = 1
        minute = sec * 60
        while True:
            i = 0 if i > 600 else i
            try:
                if i and not i % sec:
                    Checker.check_ssh_connections()
                if i and not i % 5 * sec:
                    Checker.check_ip()
                if i and not i % minute:
                    Checker.check_temperature()
                if i and not i % 5 * minute:
                    Checker.check_used_space()
            except Exception as _ex:
                logging.exception(f'Unrecognized exception {_ex}')
            i += 1
            time.sleep(1)

    @staticmethod
    def run():
        # хинт, что бы процессы не двоились
        if 'WERKZEUG_RUN_MAIN' not in os.environ:
            cl = threading.Thread(target=Checker.check_loop)
            cl.start()
