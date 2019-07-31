"""Sqlalchemy models."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from wtlogger.db import Base
import wtlogger.config as conf


class WorkDay(Base):
    __tablename__ = "workday"

    id = Column(Integer, primary_key=True)
    dttm = Column(DateTime)
    iso_format = Column(String, unique=True)
    work_duration = Column(Integer)
    create_at = Column(DateTime)

    def __init__(self, dttm: datetime, work_duration: int = conf.DEFAULT_DAY_DURATION):
        self.dttm = dttm.date()
        self.iso_format = dttm.strftime("%Y-%m-%d")
        self.work_duration = work_duration
        self.create_at = datetime.today()

    def __repr__(self):
        return "<WorkDay(iso_format='%s', work_duration='%s')>" % (
            self.iso_format,
            self.work_duration,
        )


class WorkSession(Base):
    __tablename__ = "work_session"

    id = Column(Integer, primary_key=True)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    created_at = Column(DateTime)
    event = relationship("Event")

    def __init__(self, start_at, end_at=None):
        self.start_at = start_at
        self.end_at = end_at
        self.created_at = datetime.today()

    def __repr__(self):
        return "<WorkSession('id='%s' started_at='%s', ended_at='%s')>" % (
            self.id,
            self.create_at,
            self.ended_at,
        )


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("work_session.id"))
    type_id = Column(Integer, ForeignKey("event_type.id"))
    created_at = Column(DateTime)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    note = Column(String)

    # def __init__(self, ):
    # pass

    def __repr__(self):
        return "<Event(name='%s', type='%s', created_at='%s', ended_at='%s')>" % (
            self.name,
            self.type_id,
            self.created_at,
            self.end_at,
        )


class EventType(Base):
    __tablename__ = "event_type"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_at = Column(DateTime)
    default_duration = Column(Integer)
    is_work_time = Column(Boolean)
    is_active = Column(Boolean)
    event = relationship("Event")

    def __init__(
        self, name, is_work_time, default_duration=conf.DEFAULT_EVENT_DURATION
    ):
        self.name = name
        self.create_at = datetime.today()
        self.default_duration = default_duration
        self.is_work_time = is_work_time
        self.is_active = True

    def __repr__(self):
        return "<EventType(name='%s'>" % (self.name)
