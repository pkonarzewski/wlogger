"""Sqlalchemy models."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

import wtl.config as conf


Base = declarative_base()
metadata = Base.metadata


def db_connect(uri=conf.DATABASE_URI):
    return create_engine(uri)


def create_table(engine):
    Base.metadata.create_all(engine)


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    dttm = Column(DateTime, nullable=False)
    action_name = Column(String)

    def __repr__(self):
        str_created_at = self.created_at.dttm("%Y-%m-%d %H:%M:%S")
        return "<Entry(dttm='%s', action='%s')>" % str_created_at, self.action_name

    def log_action(self, session, action_type, dttm):
        pass


# class WorkDay(Base):
#     __tablename__ = 'work_day'

#     id = Column(Integer, primary_key=True)
#     dt = Column(Date)
#     work_hour = Column(Integer)

#     def __repr__(self):
#         return "<WorkDay(dt='%s', work_hour='%s')>" % (self.dt, self.work_hour)


engine = db_connect(conf.DATABASE_URI)
metadata.create_all(engine)
