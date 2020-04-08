import contextlib
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import wtlogger.config as conf
from wtlogger.exceptions import WtlException


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


def provide_session(func):
    """
    Function decorator that provides a session if it isn't provided.
    If you want to reuse a session or run the function as part of a
    database transaction, you pass it to the function, if not this wrapper
    will create one and close it for you.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_session = "session"

        func_params = func.__code__.co_varnames
        session_in_args = arg_session in func_params and func_params.index(
            arg_session
        ) < len(args)
        session_in_kwargs = arg_session in kwargs

        if session_in_kwargs or session_in_args:
            return func(*args, **kwargs)
        else:
            with create_session() as session:
                kwargs[arg_session] = session
                return func(*args, **kwargs)

    return wrapper


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
