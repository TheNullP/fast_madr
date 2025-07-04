from http import HTTPStatus
from typing import Optional
from urllib.parse import urlparse

import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fast_madr.core.config import cloudinary
from fast_madr.core.database import Book, User, get_db
from fast_madr.core.security import token_verify

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10BM em bytes
ALLOWED_EXTENSIONS = {'image/jpeg', 'image/png', 'image/jpg'}


def get_public_id(image_url: str):
    parsed_url = urlparse(image_url)

    path = parsed_url.path

    path_parts = path.split('/')

    public_id = '/'.join(path_parts[5:])

    public_id = public_id.rsplit('.', 1)[0]

    return public_id


@router.post('/upload/profile-picture/')
async def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    auth_user: User = Depends(token_verify),
):
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail='Formato de arquivo não suportado. Use JPEG ou PNG',
        )

    file_size = await file.read()
    if len(file_size) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail='O arquivo é muito grande. O limite é 10MB.',
        )

    await file.seek(0)

    try:
        # upload para o cloudinary
        public_id = (
            get_public_id(auth_user.profile_picture)
            if auth_user.profile_picture
            else None
        )
        if public_id:
            cloudinary.uploader.destroy(public_id)

        result = cloudinary.uploader.upload(
            file.file, folder='media/profile_pictures/'
        )
        profile_url = result['secure_url']

        # Atualiza o usuário com a nova foto
        auth_user.profile_picture = profile_url
        db.commit()
        db.refresh(auth_user)

        # retorn a URL da imagem armazenada
        return {'url': profile_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/create_book', tags=['books'], status_code=HTTPStatus.CREATED)
async def upload_created_book(
    book_title: str = Form(...),
    book_year: int = Form(...),
    book_author: str = Form(...),
    book_file: UploadFile = File(...),
    book_cover: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user_auth: User = Depends(token_verify),
):
    exists_book = db.query(Book).filter_by(titulo=book_title).first()

    if exists_book:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Book already exists.'
        )

    try:
        result = cloudinary.uploader.upload(
            book_file.file,
            resource_type='raw',
            folder='/media/book/',
        )
        book_url = result['secure_url']

        book_cover_url = None
        if book_cover:
            result_cover = cloudinary.uploader.upload(
                book_cover.file,
                folder='/media/book_cover/',
            )
            book_cover_url = result_cover['secure_url']

        new_book = Book(
            titulo=book_title,
            ano=book_year,
            author=book_author,
            id_user=user_auth.id,
            file_book=book_url,
            book_cover=book_cover_url,
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={f'Erro na criação do livro: {e}'},
        )

    return JSONResponse(
        content={
            'msg': 'Livro criado com sucesso!',
            'book_id': new_book.id,
        },
        status_code=HTTPStatus.CREATED,  # 201
    )
