import configparser
from collections import namedtuple
from pathlib import Path
import logging


MODULE_DOT_PATH = Path().home() / '.wlogger'

if MODULE_DOT_PATH.exists() is False:
    MODULE_DOT_PATH.mkdir()

CONFIG = configparser.ConfigParser()
CONFIG.read(MODULE_DOT_PATH / 'config.ini')

LOG_FILE = Path(CONFIG.get('common', option='log_file'))

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

LOGGER = logging.getLogger('worklogger')
hdlr = logging.FileHandler(MODULE_DOT_PATH / 'logs.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOGGER.addHandler(hdlr)
LOGGER.setLevel(logging.INFO)

SQL_URL = 'sqlite:///' + str(MODULE_DOT_PATH / 'data.db')
