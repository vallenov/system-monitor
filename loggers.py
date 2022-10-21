import logging
import os

logging.basicConfig(level=logging.INFO)


def get_logger(name: str, file_name: str = 'run.log'):
    curdir = os.curdir
    if not os.path.exists(os.path.join(curdir, 'services')):
        os.mkdir(os.path.join(curdir, 'services'))
        os.chown(os.path.join(curdir, 'services'), 1000, 1000)
        os.system(f'touch {os.path.join(curdir, "services", "deploy.log")}')
        os.system(f'chmod 755 {os.path.join(curdir, "services", "deploy.log")}')
    logger = logging.getLogger(name)
    handler = logging.FileHandler(file_name)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger
