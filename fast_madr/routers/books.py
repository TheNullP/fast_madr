from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fast_madr.security import token_verify

from fast_madr.models import Book, User, get_db
from fast_madr.schema import BookModel


router = APIRouter()


@router.get("/read-book", tags=["books"])
def read_books(db: Session = Depends(get_db)): 
    q = db.query(Book).order_by(Book.id).all()

    return q


@router.post("/book/{user_id}/", tags=["books"], status_code=HTTPStatus.CREATED)
def create_book( book: BookModel, author_id: int, db: Session = Depends(get_db),user_auth: User = Depends(token_verify),):
    exists_user = db.get(User, user_auth.id)

    if not exists_user:
        raise HTTPException(status_code=404, detail="User not found.")
    new_book = Book(
        titulo=book.titulo,
        ano=book.ano,
        id_author=author_id,
        id_user=user_auth.id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return JSONResponse(
        content={'msg': 'success.'},
        status_code=201,
    )


@router.put("/book/{user_id}/{book_id}", tags=["books"])
def update_book(
    book_id: int, 
    book: BookModel,
    db: Session = Depends(get_db),
    user_auth: User = Depends(token_verify)
):
    existed_user_and_book = (
        db.query(Book).where(Book.id == book_id and Book.id_user == user_auth.id).first()
    )
    if not existed_user_and_book:
        raise HTTPException(status_code=404, detail="Book or User not found.")

    existed_user_and_book.titulo = book.titulo
    existed_user_and_book.ano = book.ano

    db.commit()
    db.refresh(existed_user_and_book)

    return JSONResponse(
        content={},
        status_code=200
    )


@router.delete("/book/{user_id}/{book_id}", tags=["books"])
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    user_auth: User = Depends(token_verify)
):
    existed_user_and_book = (
        db.query(Book).where(Book.id == book_id and Book.id_user == user_auth.id).first()
    )

    if not existed_user_and_book:
        raise HTTPException(status_code=404, detail="Book or User not found.")
    db.delete(existed_user_and_book)
    db.commit()

    return {"detail": "Book deleted."}

router.get('/books', response_model=List[dict])
def get_books(page: int =1, per_page: int = 10, db: Session= Depends(get_db)):
    books = db.query(Book).all()

    start = (page - 1) * per_page
    end = start + per_page
    return books[start:end]
