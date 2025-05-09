from http import HTTPStatus
from urllib.parse import urlparse

import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fast_madr.core.config import cloudinary
from fast_madr.core.database import Book, User, get_db
from fast_madr.core.security import token_verify

router = APIRouter()

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2BM em bytes
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
            status_code=400, detail='O arquivo é muito grande. O limite é 2MB.'
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
def create_book(
    titulo: str = Form(...),
    ano: int = Form(...),
    author: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_auth: User = Depends(token_verify),
):
    exists_book = db.query(Book).filter_by(titulo=titulo).first()

    if exists_book:
        raise HTTPException(status_code=400, detail='Book already exists.')

    result = cloudinary.uploader.upload(file.file, folder='/media/book/')
    book_url = result['secure_url']

    new_book = Book(
        titulo=titulo,
        ano=ano,
        author=author,
        id_user=user_auth.id,
        file_book=book_url,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return JSONResponse(
        content={'msg': 'success.'},
        status_code=201,
    )
