from typing_extensions import List
from pydantic import BaseModel
from pydantic.fields import Field


class UserModel(BaseModel):
    username: str
    email: str = Field(default="email@email.com")
    password: str


class UserPublic(UserModel):
    username: str
    emai: str = Field(default="email@email.com")


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
    



class Token(BaseModel):
    access_toke: str
    token_type: str
class LoginModel(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    username: str
    email: str
