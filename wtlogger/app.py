from datetime import datetime, date, timedelta, timezone
from typing import Optional, Dict

from sqlalchemy import func
from sqlalchemy.orm import exc
from sqlalchemy.orm.session import Session
import pendulum

import wtlogger.config as conf
from wtlogger.db import create_session, provide_session
from wtlogger.models import WorkInterval
from wtlogger.exceptions import WtlException


class WorkLogger:
    """Class responsible for logging all events and computing stats."""

    def __init__(self, tz: str = conf.TIMEZONE):
        self.tz = pendulum.timezone(conf.TIMEZONE)

    @provide_session
    def start_work(self, dttm: datetime, session: Optional[Session] = None) -> None:
        last_interval = self.get_last_work_interval(session)

        if last_interval is not None and last_interval.is_active:
            raise WtlException(f"There is still open work interval {last_interval}")
        else:
            session.add(WorkInterval(started_at=self.format_dttm(dttm)))

    @provide_session
    def stop_work(self, ddtm: datetime, session: Optional[Session] = None) -> None:
        last_interval = self.get_last_work_interval(session)

        if not last_interval.is_active:
            raise WtlException("No open work interval to close.")
        else:
            last_interval.ended_at = self.format_dttm(ddtm)

    def format_dttm(self, dttm: str) -> datetime:
        if dttm == "now":
            dttm = pendulum.now(tz=self.tz)
        else:
            dttm = pendulum.parse(dttm, tz=self.tz)
        return dttm.replace(microsecond=0)

    @provide_session
    def get_last_work_interval(self, session: Optional[Session] = None):
        query = session.query(WorkInterval).order_by(WorkInterval.started_at.desc())
        return query.first()

    @provide_session
    def show_last_intervals(
        self, dttm: datetime, n: int = 5, session: Optional[Session] = None
    ):
        ses = reversed(
            session.query(WorkInterval)
            .filter(func.DATE(WorkInterval.started_at) <= func.DATE(dttm))
            .order_by(WorkInterval.started_at.desc())
            .limit(n)
            .all()
        )
        for s in ses:
            print("|", s.id, "|", s.started_at, "|", s.ended_at, "|")

        return ses

    @provide_session
    def workday_status(self, dttm: datetime, session: Optional[Session] = None):
        """X."""
        selected_intervals = session.query(WorkInterval).filter(
            func.DATE(WorkInterval.started_at) == func.DATE(dttm)
        )

        w_duration = pendulum.duration(
            seconds=sum([x.duration for x in selected_intervals])
        )
        if w_duration.seconds > 0:
            first_start = (
                selected_intervals.order_by(WorkInterval.started_at).first().started_at
            )
            workday_duration = pendulum.duration(minutes=conf.DEFAULT_WORKDAY_DURATION)
            planed_end = first_start + workday_duration
            remaining = workday_duration - w_duration

        self.print_status(
            data={
                "first_start": first_start,
                "planned_end": planed_end,
                "w_duration": w_duration,
                "remaining": remaining,
                "workday_duration": workday_duration,
            }
        )

    def print_status(self, data: Dict):

        if data is not None:

            # TODO: extract responsiblity to other class
            if data["w_duration"] <= data["workday_duration"]:
                wee_text = "Remaning"
            else:
                wee_text = "Overtime"

            status_template = (
                f"At work from:\t {data['first_start']:%H:%M:%S}",
                f"\nPlanned end at:\t {data['planned_end']:%H:%M:%S}",
                "\n=========================",
                f"\nWork duration:\t {data['w_duration']}",
                f"\n{wee_text}:\t {data['remaining']}",
            )
            print("".join(status_template))
        else:
            print("No data")
