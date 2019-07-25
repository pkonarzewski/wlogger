import contextlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import wtlogger.config as conf


log = conf.LOGGER

engine = create_engine(conf.DATABASE_URI, echo=conf.SQLALCHEMY_ECHO)
Base = declarative_base()
Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
)


@contextlib.contextmanager
def create_session():
    """Contextmanager that will create and teardown a session.

    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def initdb():
    """x."""
    log.info("Init database")
    upgradedb()


def upgradedb():
    """x."""
    # TODO: alembic
    log.info("Creating tables")
    Base.metadata.create_all(engine)


def resetdb():
    """x."""
    log.info("TODO: Reset database")
