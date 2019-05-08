"""x."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class ActionType(Base):
    __tablename__ = 'action_type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<ActionType(name='%s')>" % self.name


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    action_id = Column(Integer, ForeignKey('action_type.id'))
    dttm = Column(DateTime, nullable=False)

    action = relationship('action_type', back_populates='entry')

    def __repr__(self):
        return "<Entry(dttm='%s')>" % self.dttm


class WorkDay(Base):
    __tablename__ = 'work_day'

    id = Column(Integer, primary_key=True)
    dt = Column(Date)
    work_hour = Column(Integer)

    def __repr__(self):
        return "<WorkDay(dt='%s', work_hour='%s')>" % (self.dt, self.work_hour)
