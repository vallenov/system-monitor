import os
import subprocess as sp

import config

from cron import cron
from loggers import get_logger

logger = get_logger(__name__)


class Deploy:

    @staticmethod
    @cron(rule=config.CronTab.deploy)
    def activate_deploy(**kwargs):
        """
        Autodeploy projects from GitHub
        """
        for project_name, service_name in config.DeployConf.projects.items():
            Deploy.deploy_project(project_name, service_name)
        Deploy.self_deploy()

    @staticmethod
    def deploy_project(project_name, service_name):
        try:
            curr_project_dir = os.path.join(os.path.join(config.DeployConf.projects_dir, project_name))
            os.chdir(curr_project_dir)
            pull = sp.check_output('git pull', shell=True).decode().replace('\n', '')
            if pull != 'Already up to date.':
                logger.info(f'Update found for {project_name}')
                if 'requirements.txt' in os.listdir(curr_project_dir):
                    logger.info('Updating...')
                    if '.venv' in os.listdir(curr_project_dir):
                        os.system('. ./.venv/bin/activate && ./.venv/bin/pip install -r requirements.txt')
                    else:
                        os.system(f'pyenv activate {project_name} && pip install -r requirements.txt')
                    os.system(f'systemctl restart {service_name}.service')
                    logger.info(f'Update {project_name} complete\n')
                else:
                    raise FileNotFoundError('requirements.txt')
            else:
                logger.info(f'Update not found for {project_name}')
        except FileNotFoundError:
            logger.exception()

    @staticmethod
    def self_deploy():
        Deploy.deploy_project('system-monitor', 'system_monitor')

    @staticmethod
    def run(now_dict=None):
        Deploy.activate_deploy(now_dict=now_dict)


if __name__ == "__main__":
    Deploy.deploy_project('system-monitor', 'system_monitor')