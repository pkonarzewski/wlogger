"""The main config file.

All configuration in this file can be overridden by providing a config file in ~/.wtl
"""

import os
import sys
import imp
import logging
from collections import namedtuple
import logging


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if "WTL_HOME" in os.environ:
    DATA_PATH = os.environ["WTL_HOME"]
else:
    DATA_PATH = os.path.join(os.path.expanduser("~"), '.wtl')


# ------------------------------------------------------------------------------
# SETTINGS

# Date format for all logs
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# The SQLAlchemy connection string.
DATABASE_URI = 'sqlite:///' + os.path.join(DATA_PATH, 'data.db')

# Logger file path
LOG_FILE = os.path.join(DATA_PATH, 'logs.log')

# Log settings
LOG_FORMAT = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
LOG_LEVEL = 'DEBUG'

# Worklog #TODO: migrate to db and remove
WORKLOG_FILE = os.path.join(DATA_PATH, 'worklog.csv')
ROW = namedtuple('row', ['date', 'action'])

# Logger object
LOGGER = logging.getLogger(__name__)

hdlr = logging.FileHandler(LOG_FILE)
hdlr.setFormatter(LOG_FORMAT)

LOGGER.addHandler(hdlr)
LOGGER.setLevel(LOG_LEVEL)


# Config overried by local file
config_path = os.path.join(DATA_PATH, 'config.py')
if os.path.exists(config_path):
    module = sys.modules[__name__]
    override_conf = imp.load_source('config', config_path)

    for key in dir(override_conf):
        if key.isupper():
            setattr(module, key, getattr(override_conf, key))
