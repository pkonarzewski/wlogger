"""
Work Time Logger.
"""

import logging
from pathlib import Path
from datetime import datetime, timedelta
from collections import namedtuple


# GENERATOR?
class Worklog(object):

    def __init__(self, fpath):
        self.log = open("foo.txt", "rw+")
        pass

    def __del__(self):
        self.log.close()

    # def get_state(self):
    #     # working, off, overtime
    #     pass

    # def set_state(self, state, date):
    #     pass

    def seek(self):
        pass

    def get_date_position(self):
        pass


class Reporter(object):

    def __init__(self):
        pass


class WTL(object):

    def __init__(self, output_path, logger):
        pass

    def start(self, date):
        pass

    def stop(self, date):
        pass

    def status(self):
        pass

    def get_current_state(self):
        pass

    def report(self):
        pass

    def bye(self):
        pass
