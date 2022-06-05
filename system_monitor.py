import requests
import configparser
import logging
import time

from monitor_classes import Monitor

MAX_TRY = 15


def load_config():
    config = configparser.ConfigParser()
    config.read('system_monitor.ini', encoding='utf-8')
    return config


def ini_save(config_inf):
    '''
    Сохранение изменений в іnі-файл
    '''
    with open(f'system_monitor.ini', 'w') as f:
        config_inf.write(f)


conf = load_config()


def send_message(data: dict):
    """
    Отправка сообщения админу

    """
    current_try = 0
    while current_try < MAX_TRY:
        current_try += 1
        try:
            requests.post(conf.get('URL', 'message_server_address') + 'telegram',
                          data=data,
                          headers={'Connection': 'close'})
        except Exception as exc:
            logging.exception(exc)
        else:
            logging.info('Send successful')
            break
    logging.error('Max try exceeded')


def check_temperature():
    """
    Проверка превышения заданной температуры
    """

    max_temp = int(conf.get('MAX_VALUES', 'max_temp'))

    temp = Monitor.get_temperature()
    if temp >= max_temp and Monitor.block_message.get('temperature', False) is False:
        data = dict()
        data['to'] = conf.get('CONTACT', 'telegram_name')
        name = Monitor.get_name_of_machine()
        data['text'] = f'Температура {name} сейчас: {temp}°C'
        send_message(data)
        logging.info('Send successful')
        Monitor.block_message['temperature'] = True
    elif temp < max_temp:
        Monitor.block_message['temperature'] = False


def check_ssh_connections():
    """
    Проверка ssh соединений
    """
    connections = Monitor.get_ssh_connections()
    for conn in Monitor.block_message['ssh'].keys():
        if conn not in connections:
            Monitor.block_message['ssh'].pop(conn)
    for conn in connections:
        if len(connections) == 1 and Monitor.block_message.get('ssh', {}).get(conn, False) is False:
            data = dict()
            data['to'] = conf.get('CONTACT', 'telegram_name')
            name = Monitor.get_name_of_machine()
            data['text'] = f'Новое подключение к "{name}" с адреса {conn}'
            send_message(data)
            Monitor.block_message['ssh'][conn] = True
        elif len(connections) > 1:
            data = dict()
            data['to'] = conf.get('CONTACT', 'telegram_name')
            name = Monitor.get_name_of_machine()
            data['text'] = f'Количество подключений к "{name}" превысило 1! Текущие соединения: {connections}'
            send_message(data)
            for c in connections:
                Monitor.block_message['ssh'][c] = True
        elif len(connections) == 0:
            Monitor.block_message['ssh'].clear()


def check_used_space():
    """
    Проверка оставшегося свободного места на жестком диске
    """
    max_used_space = int(conf.get('MAX_VALUES', 'max_used_space'))
    used_space = Monitor.get_used_space()
    name = Monitor.get_name_of_machine()
    for key, value in used_space.items():
        if value > max_used_space and Monitor.block_message.get('used_space').get(key, False) is False:
            data = dict()
            data['to'] = conf.get('CONTACT', 'telegram_name')
            data['text'] = f'Свободное место в "{key}" на сервере {name} заканчивается. Осталось {100 - value}%'
            send_message(data)
            Monitor.block_message['used_space'][key] = True
        elif value < max_used_space:
            Monitor.block_message['used_space'][key] = False


def check_ip():
    """
    Проверка изменения IP-адреса
    """
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
    data['to'] = conf.get('CONTACT', 'telegram_name')
    data['text'] = f'Новый IP-адрес {name}: {new_ip}'
    send_message(data)


if __name__ == "__main__":
    logging.basicConfig(filename='run.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    i = 0
    sec = 1
    minute = sec * 60

    while True:
        i = 0 if i > 600 else i
        try:
            if i and not i % 5*sec:
                check_ip()
                check_ssh_connections()
            if i and not i % minute:
                conf = load_config()
                check_temperature()
            if i and not i % 5*minute:
                check_used_space()
        except Exception as _ex:
            logging.exception(f'Unrecognized exception {_ex}')
        i += 1
        time.sleep(1)

