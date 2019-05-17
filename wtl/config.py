"""The main config file.

All configuration in this file can be overridden by providing a config file in ~/.wtl
"""

import sys
import imp
import logging
from collections import namedtuple
from pathlib import Path
import logging


# ------------------------------------------------------------------------------
# SETTINGS

# Folder for package
DATA_PATH = Path().home() / '.wtl'

# Date format for all logs
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# The SQLAlchemy connection string.
DATABASE_URI = 'sqlite:///' + str(DATA_PATH / 'data.db')

# Logger file path
LOG_FILE = DATA_PATH / 'logs.log'

# Log settings
LOG_FORMAT = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
LOG_LEVEL = 'DEBUG'

# Worklog #TODO: migrate to db and remove
WORKLOG_FILE = DATA_PATH / 'worklog.csv'
ROW = namedtuple('row', ['date', 'action', 'info'])

# Config overried by local file
config_path = Path(DATA_PATH / 'config.py')
if config_path.exists():
    module = sys.modules[__name__]
    override_conf = imp.load_source('config', str(config_path))

    for key in dir(override_conf):
        if key.isupper():
            setattr(module, key, getattr(override_conf, key))


# ------------------------------------------------------------------------------
# SETUP
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True)

if not Path(WORKLOG_FILE).exists():
    with Path(WORKLOG_FILE).open(mode='w', encoding='utf8') as f:
        f.write('date;action;info\n')


# ------------------------------------------------------------------------------
# LOGGER
LOGGER = logging.getLogger(__name__)

hdlr = logging.FileHandler(LOG_FILE)
hdlr.setFormatter(LOG_FORMAT)

LOGGER.addHandler(hdlr)
LOGGER.setLevel(LOG_LEVEL)
