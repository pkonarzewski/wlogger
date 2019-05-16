import os
from datetime import datetime
from subprocess import run
import platform

import wtl.config as conf


def system_shutdown(freeze=10):
    """Shutdown system."""

    sys_name = platform.system()

    conf.LOGGER.info('Shutting down system.')

    if sys_name.upper() == 'WINDOWS':
        run("shutdown /s /t {}".format(freeze), shell=True)
    else:
        conf.LOGGER.exception('Operating system "{}" not supported'.format(sys_name))


def normalize_time(dtime):
    if isinstance(dtime, str):
        dtime = datetime.strptime(dtime, conf.DATE_FORMAT)
    dt = dtime.replace(microsecond=0)
    return dt
