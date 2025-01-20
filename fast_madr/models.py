from sqlalchemy.orm import Mapped, mapped_column, registry, sessionmaker
from sqlalchemy import ForeignKey, create_engine
from decouple import config


reg = registry()

engine = create_engine(config('DB_URL'))


@reg.mapped_as_dataclass
class User:
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


@reg.mapped_as_dataclass
class Novelist:
    __tablename__ = "novelists"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)


@reg.mapped_as_dataclass
class Book:
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str] = mapped_column(unique=True)
    ano: Mapped[int]
    id_author: Mapped[int] = mapped_column(ForeignKey("novelists.id"))
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))


Session = sessionmaker(engine)
reg.metadata.create_all(engine)


# funcao de controle da sessao
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
