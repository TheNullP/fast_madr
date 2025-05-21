from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fast_madr.core.database import Book, User, get_db
from fast_madr.core.security import token_verify
from fast_madr.schemas.book_schema import (
    BookModel,
    InfoBook,
    PaginatedBooksResponse,
)

router = APIRouter()


@router.get('/read-book', tags=['books'])
def read_books(db: Session = Depends(get_db)):
    q = db.query(Book).order_by(Book.id).all()

    return q


@router.put('/book/{user_id}/{book_id}', tags=['books'])
def update_book(
    book_id: int,
    book: BookModel,
    db: Session = Depends(get_db),
    user_auth: User = Depends(token_verify),
):
    existed_user_and_book = (
        db.query(Book)
        .where(Book.id == book_id and Book.id_user == user_auth.id)
        .first()
    )
    if not existed_user_and_book:
        raise HTTPException(status_code=404, detail='Book or User not found.')

    existed_user_and_book.titulo = book.titulo
    existed_user_and_book.ano = book.ano

    db.commit()
    db.refresh(existed_user_and_book)

    return JSONResponse(content={}, status_code=200)


@router.delete('/book/{user_id}/{book_id}', tags=['books'])
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    user_auth: User = Depends(token_verify),
):
    existed_user_and_book = (
        db.query(Book)
        .where(Book.id == book_id and Book.id_user == user_auth.id)
        .first()
    )

    if not existed_user_and_book:
        raise HTTPException(status_code=404, detail='Book or User not found.')
    db.delete(existed_user_and_book)
    db.commit()

    return {'detail': 'Book deleted.'}


@router.get('/books', response_model=PaginatedBooksResponse, tags=['books'])
def get_books(
    page: int = 1, per_page: int = 10, db: Session = Depends(get_db)
):
    start = (page - 1) * per_page

    books = db.query(Book).offset(start).limit(per_page).all()

    total_books = db.query(Book).count()

    return {'books': books, 'total_books': total_books}


@router.get('/page_book', tags=['books'])
def get_page_book(
    id_book: int,
    db: Session = Depends(get_db),
):
    inf_book = db.query(Book).filter_by(id=id_book).first()
    if not inf_book:
        return JSONResponse(
            content={'msg': 'Livro não encontrado.'},
            status_code=HTTPStatus.NOT_FOUND,
        )
    try:
        creator = db.query(User).filter_by(id=inf_book.id_user).first()
        book = InfoBook(
            titulo=inf_book.titulo,
            ano=inf_book.ano,
            author=inf_book.author,
            criado_por=creator.username,
            url=inf_book.file_book,
        )

        return book

    except Exception as e:
        raise e
