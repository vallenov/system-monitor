import config
from cron import cron


class Backup:

    @cron(rule=config.CronTab.backup)
    def activate_backup(self):
        pass

    @staticmethod
    def run(now_dict=None):
        Backup.activate_backup(now_dict=now_dict)