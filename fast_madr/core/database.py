from decouple import config
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import Mapped, mapped_column, registry, sessionmaker

from fast_madr.core.settings import Settings

reg = registry()
settings = Settings()

engine = create_engine(settings.DB_URL)


@reg.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    profile_picture: Mapped[str] = mapped_column(
        String, init=False, nullable=True
    )


@reg.mapped_as_dataclass
class Author:
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)


@reg.mapped_as_dataclass
class Book:
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str] = mapped_column(unique=True)
    ano: Mapped[int]
    author: Mapped[str]
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    file_book: Mapped[str] = mapped_column(unique=True)
    book_cover: Mapped[str] = mapped_column(String, nullable=True)


Session = sessionmaker(engine)
reg.metadata.create_all(engine)


# funcao de controle da sessao
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
