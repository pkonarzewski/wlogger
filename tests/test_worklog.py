import unittest

from wtlogger import Worklog


class TestWorkLog(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        wtl = Worklog()
