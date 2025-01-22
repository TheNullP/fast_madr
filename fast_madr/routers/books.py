from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fast_madr.models import Author, Book, User, get_db
from fast_madr.schema import BookModel, PaginatedBooksResponse
from fast_madr.security import token_verify


router = APIRouter()


@router.get("/read-book", tags=["books"])
def read_books(db: Session = Depends(get_db)): 
    q = db.query(Book).order_by(Book.id).all()

    return q


@router.post("/book/{user_id}/", tags=["books"], status_code=HTTPStatus.CREATED)
def create_book( book: BookModel, name_author: str, db: Session = Depends(get_db),user_auth: User = Depends(token_verify),):
    exists_author = db.query(Author).filter_by(nome=name_author).first()
    exists_book = db.query(Book).filter_by(titulo=book.titulo).first()

    if exists_author is None:
        raise HTTPException(status_code=404, detail="Author not found.")

    if exists_book:
        raise HTTPException(status_code=400, detail="Book already exists.")

    new_book = Book(
        titulo=book.titulo,
        ano=book.ano,
        author=exists_author.nome,
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

@router.get("/books", response_model=PaginatedBooksResponse, tags=["books"])
def get_books(page: int =1, per_page: int = 10, db: Session= Depends(get_db)):
    start = (page - 1) * per_page

    books = db.query(Book).offset(start).limit(per_page).all()

    total_books = db.query(Book).count()

    return {'books': books, 'total_books': total_books}
