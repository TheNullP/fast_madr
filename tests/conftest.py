import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_madr.models import get_db, reg, User
from fast_madr.security import get_password_hash
from fast_madr.main import app


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def db_session(engine):
    reg.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    reg.metadata.drop_all(engine)


@pytest.fixture
def client(db_session):
    # SESSION DE TEST QUE VAI SOBRESCREVER O DB
    def get_session_override():
        return db_session

    with TestClient(app) as client:
        app.dependency_overrides[get_db] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(db_session):
    pwd = 'testtest'
    user = User(
        username='test',
        email='test@test.com',
        password=get_password_hash(pwd)
        
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    user.clean_password = pwd # Monkey Patch

    return user



