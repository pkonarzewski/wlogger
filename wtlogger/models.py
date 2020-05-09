from typing import Optional
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from wtlogger.db import Base


class WorkInterval(Base):
    __tablename__ = "work_interval"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    project_id = Column(Integer)

    def __init__(self, started_at: datetime, ended_at: Optional[datetime] = None):
        self.started_at = started_at
        self.ended_at = ended_at

    def now(self) -> datetime:
        return datetime.today().replace(microsecond=0)

    @property
    def duration(self) -> int:
        ended_at = self.now() if self.ended_at is None else self.ended_at
        return (ended_at - self.started_at).seconds

    @property
    def is_active(self) -> bool:
        return self.ended_at is None

    def __repr__(self) -> str:
        return f"<WorkInterval('id='{self.id}' started_at='{self.started_at}', ended_at='{self.ended_at}')>"
