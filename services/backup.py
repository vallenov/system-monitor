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
        if not config.BackupConf.remote_server and not os.path.exists(config.BackupConf.to_dir):
            os.makedirs(config.BackupConf.to_dir, 0o755)
        if not os.path.exists('zip'):
            os.makedirs('zip', 0o755)
        if not config.BackupConf.remote_server:
            cmd = 'cp'
            host = ''
        else:
            tunnel = Monitor.get_ngrok_tunnels()
            cmd = f"scp -P {int(tunnel['msg'][0]['port'])}"
            host = tunnel['msg'][0]['url']
            host = host.split('//')[1] + ':/'
        for item in config.BackupConf.items_to_backup:
            if os.path.isfile(item):
                path = os.path.dirname(item)
            else:
                path = item.split('/')
                path = '/'.join(path[:-1])
            if not config.BackupConf.remote_server and not os.path.exists(config.BackupConf.to_dir + path):
                os.makedirs('zip/' + path, 0o755)
            os.system(f'cp {"" if os.path.isfile(item) else "-r"} {item} zip/')
        nt = now_time()
        os.system(f'zip -r {"backup_" + nt} zip/')
        os.system(f'{cmd} '
                  f'{"backup_" + nt + ".zip"} ' 
                  f'{host + config.BackupConf.to_dir}')

    @staticmethod
    def run(now_dict=None):
        Backup.activate_backup(now_dict=now_dict)
