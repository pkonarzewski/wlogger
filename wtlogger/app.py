from datetime import datetime, date, timedelta
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import exc
from sqlalchemy.orm.session import Session

import wtlogger.config as conf
from wtlogger.db import create_session, provide_session
from wtlogger.models import WorkInterval
from wtlogger.exceptions import WtlException


class WorkLogger:
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

        # TODO: if close date is next day, close on last day, open new session

    def format_dttm(self, dttm: datetime) -> datetime:
        return dttm.replace(microsecond=0)

    @provide_session
    def get_last_work_interval(self, session: Optional[Session] = None):
        query = session.query(WorkInterval).order_by(WorkInterval.started_at.desc())
        return query.first()

    @provide_session
    def show_last_intervals(self, n: int = 5, session: Optional[Session] = None):
        ses = reversed(
            session.query(WorkInterval)
            .order_by(WorkInterval.started_at.desc())
            .limit(n)
            .all()
        )
        for s in ses:
            print("|", s.id, "|", s.started_at, "|", s.ended_at, "|")

        return ses

    def workday_status(self, dttm=datetime.today()):

        with create_session() as session:
            stats = self.compute_stats(dttm, session)

        if stats is not None:
            status_template = (
                f"W pracy od:\t {stats['first_start']:%H:%M:%S}",
                f"\nKoniec o:\t {stats['planned_end']:%H:%M:%S}",
                "\n=========================",
                f"\nTwa już:\t {stats['w_duration']}",
                f"\n{stats['wee_text']}:\t {stats['remaining']}",
            )
            print("".join(status_template))
        else:
            print("No data")

    def compute_stats(self, dttm: datetime, session: Optional[Session] = None):

        today_intervals = session.query(WorkInterval).filter(
            func.DATE(WorkInterval.started_at) == dttm.date()
        )

        w_duration = timedelta(seconds=sum([x.duration for x in today_intervals]))

        # TODO: what to do where there is no data today
        first_start = (
            today_intervals.order_by(WorkInterval.started_at).first().started_at
        )
        workday_duration = timedelta(minutes=conf.DEFAULT_WORKDAY_DURATION)
        remaining = workday_duration - w_duration
        planed_end = datetime.now() + max([timedelta(seconds=0), remaining])

        if w_duration <= workday_duration:
            wee_text = "Pozostalo"
        else:
            wee_text = "Nadgodziny"

        return {
            "first_start": first_start,
            "planned_end": planed_end,
            "wee_text": wee_text,
            "w_duration": w_duration,
            "remaining": remaining,
        }
