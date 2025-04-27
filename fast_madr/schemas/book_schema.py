from typing_extensions import List
from pydantic import BaseModel

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

