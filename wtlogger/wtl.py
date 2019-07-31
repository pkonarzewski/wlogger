"""x."""

from datetime import datetime

import wtlogger.config as conf
from wtlogger.db import create_session
from wtlogger.models import WorkDay, WorkSession, Event, EventType


class Worklog:
    pass

    def start_day(self, dttm):
        with create_session() as session:
            session.add(WorkDay(dttm=dttm))

    def start_session(self, dttm):
        with create_session() as session:
            session.add(WorkSession(start_at=dttm))

    def end_session(self, ddtm):
        with create_session() as session:
            session.query()

    def add_event(self, dttm, event_id):
        pass

    def add_event_type(self, name, default_duration, is_work_time):
        with create_session() as session:
            session.add(
                EventType(
                    name=name,
                    default_duration=default_duration,
                    is_work_time=is_work_time,
                )
            )
