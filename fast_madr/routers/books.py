from http import HTTPStatus
from typing import Optional

import cloudinary
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy import JSON
from sqlalchemy.orm import Session

from fast_madr.core.database import Book, User, get_db
from fast_madr.core.security import token_verify
from fast_madr.schemas.book_schema import InfoBook, PaginatedBooksResponse

router = APIRouter()


@router.get('/read-book', tags=['books'])
def read_books(db: Session = Depends(get_db)):
    q = db.query(Book).order_by(Book.id).all()

    return q


@router.put('/book/update', tags=['books'])
def update_book(
    book_id: int = Form(...),
    book_title: Optional[str] = Form(None),
    book_year: Optional[int] = Form(None),
    book_author: Optional[str] = Form(None),
    book_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user_auth: User = Depends(token_verify),
):
    current_book = (
        db.query(Book)
        .where(Book.id == book_id and Book.id_user == user_auth.id)
        .first()
    )
    if not current_book:
        raise HTTPException(status_code=404, detail='Book or User not found.')

    try:
        if book_title is not None:
            current_book.titulo = book_title
        if book_year is not None:
            current_book.ano = book_year
        if book_author is not None:
            current_book.author = book_author
        if book_file:
            print('Deu certo Até Aqui!!')
            cloudinary.uploader.destroy(current_book.file_book)
            result = cloudinary.uploader.upload(
                book_file.file,
                resource_type='raw',
                folder='/media/book/',
            )
            url = result['secure_url']

            current_book.file_book = url

    except Exception as e:
        print(f'Erro ao tentar Atualizar livro: {e}')
        raise HTTPException(
            status_code=500, detail=f'Erro interno do servidor: {e}'
        )

    db.commit()
    db.refresh(current_book)

    return JSONResponse(
        content={'message': 'Livro atualizado com sucesso!'}, status_code=200
    )


@router.delete('/delete_book', tags=['books'])
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

    return JSONResponse(content={'message': 'Book deleted.'}, status_code=200)


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
            id=inf_book.id,
            titulo=inf_book.titulo,
            ano=inf_book.ano,
            author=inf_book.author,
            criado_por=creator.username,
            url=inf_book.file_book,
        )

        return book

    except Exception as e:
        raise e
