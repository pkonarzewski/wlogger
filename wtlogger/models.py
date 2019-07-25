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
    work_duration = Column(Integer)

    def __repr__(self):
        return "<WorkDay(dt='%s', work_duration='%s')>" % (
            self.iso_format,
            self.work_duration,
        )


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    default_duration = Column(Integer)

    def __repr__(self):
        return "<Event(name='%s', default_duration='%s)>" % (
            self.name,
            self.default_duration,
        )


class EventLog(Base):
    __tablename__ = "eventlog"

    id = Column(Integer, primary_key=True)
    ddtm = Column(DateTime)
    start_dttm = Column(DateTime)
    day_id = Column(Integer)  #
    event_id = Column(Integer)  #
    duration = Column(Integer)  #

    def __repr__(self):
        return "<EventLog()>" % ()
