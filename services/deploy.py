import os
import subprocess as sp

import config

from cron import cron
from loggers import get_logger

logger = get_logger(__name__, 'deploy.log')


class Deploy:

    @staticmethod
    @cron(rule=config.CronTab.deploy)
    def activate_deploy(**kwargs):
        for project in config.DeployConf.projects.keys():
            try:
                curr_project_dir = os.path.join(curr_project_dir)
                os.chdir(os.path.join(config.DeployConf.projects_dir, project))
                pull = sp.check_output('git pull', shell=True)
                if pull != 'Already up to date.':
                    logger.info(f'Update found for {project}')
                    if 'requirements.txt' in os.listdir(curr_project_dir):
                        logger.info('Updating...')
                        if '.venv' in os.listdir(curr_project_dir):
                            os.system('. ./.venv/bin/activate && ./.venv/bin/pip install -r requirements.txt')
                        else:
                            os.system(f'pyenv activate {project} && pip install -r requirements.txt')
                        os.system(f'systemctl restart {config.DeployConf.projects[project]}.service')
                        logger.info(f'Update {project} complete')
                    else:
                        raise FileNotFoundError('requirements.txt')
            except FileNotFoundError as e:
                logger.exception()

    @staticmethod
    def run(now_dict=None):
        Deploy.activate_deploy(now_dict=now_dict)
