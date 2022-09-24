import os
import datetime

import config
from cron import cron
from monitor import Monitor


def now_time() -> str:
    """
    Get nowtime like: 20222-01-18123458
    """
    return str(datetime.datetime.now()).replace(':', '').replace(' ', '')[:16]


class Backup:

    @staticmethod
    @cron(rule=config.CronTab.backup)
    def activate_backup(**kwargs):
        if not config.BackupConf.activate:
            return
        if not os.path.exists(config.BackupConf.to_dir):
            os.makedirs(config.BackupConf.to_dir, 0o755)
        if not config.BackupConf.remote_server:
            cmd = 'cp'
            host = ''
        else:
            tunnel = Monitor.get_ngrok_tunnels()
            cmd = f"scp -p {tunnel['msg']['port']}"
            host = tunnel['msg']['url']
        for item in config.BackupConf.items_to_backup:
            if os.path.isfile(item):
                path = os.path.dirname(item)
            else:
                path = item.split('/')
                path = '/'.join(path[:-1])
                cmd = f'{cmd} -r'
            if not os.path.exists(config.BackupConf.to_dir + path):
                os.system(f'mkdir {config.BackupConf.to_dir + path} -p')
            os.system(f'{cmd} {os.path.join(host, item)} {config.BackupConf.to_dir + path}')
        os.system(f'zip -r {config.BackupConf.to_dir + "backup_" + now_time()} {config.BackupConf.to_dir}')

    @staticmethod
    def run(now_dict=None):
        Backup.activate_backup(now_dict=now_dict)
