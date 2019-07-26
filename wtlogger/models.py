"""Sqlalchemy models."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

import wtlogger.config as conf
from wtlogger.db import Base


class WorkDay(Base):
    __tablename__ = "workday"

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime)
    iso_format = Column(String, unique=True)
    dttm = Column(DateTime)
    work_duration = Column(Integer)
    work_session = relationship("WorkSession")

    def __repr__(self):
        return "<WorkDay(dt='%s', work_duration='%s')>" % (
            self.iso_format,
            self.work_duration,
        )


class WorkSession(Base):
    __tablename__ = "work_session"

    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("workday.id"))
    created_at = Column(DateTime)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    event = relationship("Event")

    def __repr__(self):
        return "<WorkSession('')>"


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("work_session.id"))
    type_id = Column(Integer, ForeignKey("event_type.id"))
    created_at = Column(DateTime)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    note = Column(String)

    def __repr__(self):
        return "<Event(name='%s', type='%s)>" % (self.name, self.default_duration)


class EventType(Base):
    __tablename__ = "event_type"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_at = Column(DateTime)
    default_duration = Column(Integer)
    is_work_time = Column(Boolean)
    is_active = Column(Boolean)
    event = relationship("Event")

    def __repr__(self):
        return "<EventType(name='%s'>" % (self.name)
