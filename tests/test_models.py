import pytest
from datetime import datetime

from wtlogger.models import WorkInterval
from wtlogger.app import WorkLogger


def test_get_last_interval(session):
    wl = WorkLogger()
    assert wl.get_last_work_interval(session) is None
    ws1 = WorkInterval(started_at=datetime(2000, 1, 1, 8, 0, 0))
    session.add(ws1)
    assert wl.get_last_work_interval(session) is ws1
    ws2 = WorkInterval(started_at=datetime(2000, 1, 1, 10, 0, 0))
    session.add(ws2)
    assert wl.get_last_work_interval(session) is ws2
