from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_madr.core.config import crypt_context
from fast_madr.core.database import Book, User, get_db, reg
from fast_madr.main import app


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
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
        password=crypt_context.hash(pwd),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


@pytest.fixture
def access_token(client, user):
    response = client.post(
        '/user/token',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            # necessario p/ post com data
        },
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def book(db_session, client, user):
    book = Book(
        titulo='test',
        ano=1999,
        author='test',
        id_user=user.id,
        file_book='/home/Documentos/books/book.pdf',
    )

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    return book
