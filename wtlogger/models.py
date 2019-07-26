"""Sqlalchemy models."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

import wtlogger.config as conf
from wtlogger.db import Base


class WorkDay(Base):
    __tablename__ = "workday"

    id = Column(Integer, primary_key=True)
    iso_format = Column(String, unique=True)
    dttm = Column(DateTime)
    work_duration = Column(Integer)

    def __repr__(self):
        return "<WorkDay(dt='%s', work_duration='%s')>" % (
            self.iso_format,
            self.work_duration,
        )


class WorkSession(Base):
    __tablename__ = "work_sesion"

    id = Column(Integer, primary_key=True)
    day_id = Column(Integer)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)

    def __repr__(self):
        return "<WorkSession('')>"


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    type_id = Column(Integer)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    note = Column(String)

    def __repr__(self):
        return "<Event(name='%s', type='%s)>" % (self.name, self.default_duration)


class EventType(Base):
    __tablename__ = "event_type"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    default_duration = Column(Integer)
    is_work_time = Column(Boolean)

    def __repr__(self):
        return "<EventType(name='%s'>" % (self.name)
