import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import (
    create_database,
    database_exists,
    drop_database
)

from db.base import Base
from db.db import get_db
from main import app

from backend.settings import settings

@pytest.fixture(scope="function")
def SessionLocal():
    # settings of test database
    engine = create_engine(settings.TEST_DB_URL, pool_size=3, max_overflow=0)

    assert not database_exists(settings.TEST_DB_URL), "Test database already exists. Aborting tests."

    # Create test database and tables
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Run the tests
    yield SessionLocal

    # Drop the test database
    drop_database(settings.TEST_DB_URL)

def temp_db(f):
    def func(SessionLocal, *args, **kwargs):
        #Sessionmaker instance to connect to test DB
        #  (SessionLocal)From fixture

        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        #get to use SessionLocal received from fixture_Force db change
        app.dependency_overrides[get_db] = override_get_db
        # Run tests
        f(*args, **kwargs)
        # get_Undo db
        app.dependency_overrides[get_db] = get_db
    return func
