from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fast_madr.core.database import User, get_db
from fast_madr.core.security import (
    UserLogin,
    token_verify,
    verify_activation_token,
)
from fast_madr.schemas.user_schema import LoginModel

router = APIRouter()


@router.post('/user/token', tags=['token'])
def user_login(
    form_access: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = LoginModel(
        username=form_access.username, password=form_access.password
    )

    ul = UserLogin(db=db)
    data = ul.user_login(user=user)

    return data


@router.get('/test', tags=['token'])
def test_access(token: User = Depends(token_verify)):
    return f'Its Works.{token}'


@router.get('/auth/verify-email')
def verify_email(token: str, db: Session = Depends(get_db)):

    email = verify_activation_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token inválido ou expirado.',
        )
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado.',
        )
    if user.is_active:
        return {'message': 'Esta conta já foi verificada anteriormente.'}
    user.is_active = True
    db.commit()

    return {
        'message': 'Conta ativada com sucesso! Você já pode fazer o login.'
    }
