import os
from subprocess import run
from wtl.config import LOGGER
import platform


def system_shutdown(freeze=10):
    """Shutdown system."""

    sys_name = platform.system()

    LOGGER.info('Shutting down system.')

    if sys_name == 'WINDOWS':
        run("shutdown /s /t {}".format(freeze), shell=True)
    else:
        raise Exception('Operating system {} not supported'.format(sys_name))
