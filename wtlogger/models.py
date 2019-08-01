"""Sqlalchemy models."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from wtlogger.db import Base
import wtlogger.config as conf


class WorkSession(Base):
    __tablename__ = "work_session"

    id = Column(Integer, primary_key=True)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    created_at = Column(DateTime)

    def __init__(self, start_at: datetime, end_at: datetime = None):
        self.start_at = start_at
        self.end_at = end_at
        self.created_at = datetime.now()

    def __repr__(self):
        return "<WorkSession('id='%s' start_at='%s', end_at='%s')>" % (
            self.id,
            self.start_at,
            self.end_at,
        )

    @property
    def duration(self):
        if self.end_at is None:
            end_at = datetime.today().replace(microsecond=0)
        else:
            end_at = self.end_at

        return end_at - self.start_at
