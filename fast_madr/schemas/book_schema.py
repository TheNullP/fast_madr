from pydantic import BaseModel
from typing_extensions import List


class BookModel(BaseModel):
    titulo: str
    ano: int
    author: str


class BookResponse(BaseModel):
    id: int
    titulo: str
    ano: int
    author: str
    id_user: int


class PaginatedBooksResponse(BaseModel):
    books: List[BookResponse]
    total_books: int


class InfoBook(BaseModel):
    id: int
    titulo: str
    ano: int
    author: str
    criado_por: str
    url: str
