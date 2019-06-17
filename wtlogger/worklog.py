"""."""

from pathlib import Path
from datetime import datetime
from typing import Union

import wtlogger.config as conf
from wtlogger.utils import normalize_time, system_shutdown

# from sqlalchemy.orm import sessionmaker
# from models import Deals, db_connect
# from wtlogger.models import Entry, db_connect

# def provied_session(f):
#     try:
#         session.add(entry)
#         session.commit()
#     except:
#         session.rollback()
#         raise
#     finally:
#         session.close()



def write_to_log(func):
    return None
    # with self.logfile.open(mode='a', encoding='utf8') as f:
    #     f.write(func)


class Worklog(object):

    def __init__(self, logfile: Path=conf.WORKLOG_FILE, dttm_format: str=conf.DATE_FORMAT):
        self.logfile = Path(logfile)
        self.dttm_format = dttm_format

    #     self.entry = Entry
    #     engine = db_connect()
    #     self.Session = sessionmaker(bind=engine)

    @staticmethod
    def format_dttm(dttm: datetime) -> str:
        """Format time."""
        return dttm.strftime(conf.DATE_FORMAT)

    @write_to_log
    def start(self, dttm: datetime) -> str:
        """Start work."""
        return "{};{}\n".format(self.format_dttm(dttm), 'start')

    @write_to_log
    def stop(self, dttm: datetime) -> str:
        """Stop work."""
        return "{};{}\n".format(self.format_dttm(dttm), 'stop')

    # def log(self, n):
    #     pass

    # def status(self):
    #     pass
