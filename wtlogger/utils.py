import os
from datetime import datetime
from subprocess import run
import platform
from typing import Union

import wtlogger.config as conf


def system_shutdown(freeze: int = 10) -> None:
    """Shutdown system."""

    sys_name = platform.system()

    conf.LOGGER.info("Shutting down system.")

    if sys_name.upper() == "WINDOWS":
        run("shutdown /s /t {}".format(freeze), shell=True)
    else:
        conf.LOGGER.exception('Operating system "{}" not supported'.format(sys_name))
