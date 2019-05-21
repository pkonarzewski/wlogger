"""
.
"""
from sqlalchemy.orm import sessionmaker
# from models import Deals, db_connect
from wtl.models import Entry, db_connect


def provied_session(f):
    try:
        session.add(entry)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Worklog(object):
    def __init__(self):
        self.entry = Entry
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    @provied_session
    def start(self, dttm):
        session = self.Session()
        entry=Entry(dttm=dttm, action_name='start')

    @provied_session
    def stop(self, dttm):


    @provied_session
    def log(self, n):
        pass

    @provied_session
    def status(self):
        pass
