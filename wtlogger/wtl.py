"""x."""

from datetime import datetime, date, timedelta

from sqlalchemy import func

import wtlogger.config as conf
from wtlogger.db import create_session
from wtlogger.models import WorkSession
from wtlogger.exceptions import WtlException


class Worklog:
    def start_session(self, dttm: datetime):
        with create_session() as session:
            last_session = self._get_last_session(session)

            if last_session.end_at is None:
                raise WtlException(
                    f"There is still open work session id={last_session.id}"
                )
            else:
                session.add(WorkSession(start_at=self.format_dttm(dttm)))

    def stop_session(self, ddtm: datetime):
        with create_session() as session:
            last_session = self._get_last_session(session)

            if last_session.end_at is not None:
                raise WtlException("No open work session to close.")
            else:
                last_session.end_at = self.format_dttm(ddtm)

            # TODO: if close date is next day, close on last day, open new session

    def format_dttm(self, dttm: datetime) -> datetime:
        return dttm.replace(microsecond=0)

    def _get_last_session(self, session):
        last_session = (
            session.query(WorkSession).order_by(WorkSession.created_at.desc()).first()
        )
        return last_session

    def show_last_sessions(self, n=5):

        with create_session() as session:
            ses = reversed(
                session.query(WorkSession)
                .order_by(WorkSession.created_at.desc())
                .limit(n)
                .all()
            )
            for s in ses:
                print("|", s.id, "|", s.start_at, "|", s.end_at, "|")

            return ses

    def workday_status(self, dt=date.today()):

        with create_session() as session:
            today_session = session.query(WorkSession).filter(
                func.DATE(WorkSession.start_at) == dt.strftime("%Y-%m-%d")
            )

            w_duration = timedelta(seconds=0)
            for s in today_session:
                w_duration += s.duration

            first_start = (
                today_session.order_by(WorkSession.created_at).first().start_at
            )
            work_duration = timedelta(minutes=8 * 60)
            planed_end = first_start + work_duration
            remaining = work_duration - w_duration

            if w_duration <= work_duration:
                wee_text = "Pozostalo"
            else:
                wee_text = "Nadgodziny"

        status_template = (
            "W pracy od:\t",
            first_start.strftime("%H:%m:%d"),
            "\nKoniec o:\t",
            planed_end.strftime("%H:%m:%d"),
            "\n{}:\t {}".format(wee_text, remaining),
        )

        print("".join(status_template))
