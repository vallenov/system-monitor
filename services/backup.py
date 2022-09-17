import os

import config
from cron import cron
from monitor import Monitor


class Backup:

    @staticmethod
    @cron(rule=config.CronTab.backup)
    def activate_backup(**kwargs):
        if not os.path.exists(config.BackupConf.to_dir):
            os.mkdir(config.BackupConf.to_dir)
        if not config.BackupConf.remote_server:
            cmd = 'cp'
            prefix = ''
        else:
            cmd = 'scp'
            tunnel = Monitor.get_ngrok_tunnels()
            prefix = f"{tunnel['msg']['url']}:{tunnel['msg']['port']}"
        for item in config.BackupConf.items_to_backup:
            if os.path.isfile(item):
                path = os.path.dirname(item)
            else:
                path = item.split('/')
                path = '/'.join(path[:-1])
                cmd = f'{cmd} -r'
            if not os.path.exists(config.BackupConf.to_dir + path):
                os.system(f'mkdir {config.BackupConf.to_dir + path} -p')
            os.system(f'{cmd} {os.path.join(prefix, item)} {config.BackupConf.to_dir + path}')

    @staticmethod
    def run(now_dict=None):
        Backup.activate_backup(now_dict=now_dict)
