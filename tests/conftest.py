import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from wtlogger.models import Base


@pytest.fixture(autouse=True)
def env_setup(monkeypatch, tmpdir):
    directory = str(tmpdir)
    monkeypatch.setenv("WTL_HOME", directory)
    monkeypatch.setenv("WTL__DATABASE_URI", "sqlite:///")


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///")


@pytest.yield_fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.yield_fixture
def session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
