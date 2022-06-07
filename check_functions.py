import logging

from monitor_classes import Monitor
from ini_service import load_config, ini_save
from send_service import send_message


def check_temperature():
    """
    Проверка превышения заданной температуры
    """
    conf = load_config()
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
    conf = load_config()
    connections = Monitor.get_ssh_connections()
    for conn in Monitor.block_message['ssh'].keys():
        if conn not in connections:
            Monitor.block_message['ssh'].pop(conn)
    for conn in connections:
        if Monitor.block_message.get('ssh', {}).get(conn, False) is False:
            data = dict()
            data['to'] = conf.get('CONTACT', 'telegram_name')
            name = Monitor.get_name_of_machine()
            data['text'] = str(f'Новое подключение к "{name}" с адреса {conn}.'
                               f'Текущее количество подключений: {len(connections)}')
            send_message(data)
            Monitor.block_message['ssh'][conn] = True
        elif len(connections) == 0:
            Monitor.block_message['ssh'].clear()


def check_used_space():
    """
    Проверка оставшегося свободного места на жестком диске
    """
    conf = load_config()
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
    data['to'] = conf.get('CONTACT', 'telegram_name')
    data['text'] = f'Новый IP-адрес {name}: {new_ip}'
    send_message(data)