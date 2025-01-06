from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fast_madr.security import token_verify

from fast_madr.models import Book, User, get_db
from fast_madr.schema import BookModel


router = APIRouter()


@router.get("/books/", tags=["books"])
def read_books(db: Session = Depends(get_db)): 
    q = db.query(Book).order_by(Book.id).all()

    return q


@router.post("/book/{user_id}/", tags=["books"], status_code=HTTPStatus.CREATED)
def create_book(book: Book, user_id: int, db: Session = Depends(get_db)):
    exists_book = db.get(User, user_id)

    if not exists_book:
        raise HTTPException(status_code=404, detail="User not found.")
    new_book = Book(
        titulo=book.titulo,
        ano=book.ano,
        id_user=user_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {"titulo": book.titulo, "ano": book.ano, "id_user": user_id}


@router.put("/book/{user_id}/{book_id}", tags=["books"])
def update_book(
    book_id: int, user_id: int,
    book: BookModel,
    db: Session = Depends(get_db),
    token: User = Depends(token_verify)
):
    existed_user_and_book = (
        db.query(Book).where(Book.id == book_id and Book.id_user == user_id).first()
    )
    if not existed_user_and_book:
        raise HTTPException(status_code=404, detail="Book or User not found.")

    existed_user_and_book.titulo = book.titulo
    existed_user_and_book.ano = book.ano

    db.commit()
    db.refresh(existed_user_and_book)

    return {"titulo": book.titulo, "ano": book.ano, "id_user": user_id}


@router.delete("/book/{user_id}/{book_id}", tags=["books"])
def delete_book(
    book_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    token: User = Depends(token_verify)
):
    existed_user_and_book = (
        db.query(Book).where(Book.id == book_id and Book.id_user == user_id).first()
    )

    if not existed_user_and_book:
        raise HTTPException(status_code=404, detail="Book or User not found.")
    db.delete(existed_user_and_book)
    db.commit()

    return {"detail": "Book deleted."}
