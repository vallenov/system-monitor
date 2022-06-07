import configparser


def load_config():
    config = configparser.ConfigParser()
    config.read('system_monitor.ini', encoding='utf-8')
    return config


def ini_save(config_inf):
    """
    Сохранение изменений в іnі-файл
    """
    with open(f'system_monitor.ini', 'w') as f:
        config_inf.write(f)
