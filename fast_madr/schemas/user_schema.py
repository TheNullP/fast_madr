from pydantic import BaseModel
from pydantic.fields import Field


class UserModel(BaseModel):
    username: str
    email: str = Field(default="email@email.com")
    password: str


class UserPublic(UserModel):
    username: str
    emai: str = Field(default="email@email.com")


class Token(BaseModel):
    access_toke: str
    token_type: str


class LoginModel(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    username: str
    email: str
    number_of_books: int
    created_books: list 

