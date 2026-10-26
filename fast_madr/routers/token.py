from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fast_madr.core.config import templates
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


@router.get('/auth/verify-email', response_class=HTMLResponse)
def verify_email(request: Request, token: str, db: Session = Depends(get_db)):

    email = verify_activation_token(token)
    if not email:
        return templates.TemplateResponse(
            '/activation.html',
            {
                'request': request,
                'detail': 'Token inválido ou expirado.',
                'status': 'error',
            },
        )
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return templates.TemplateResponse(
            '/activation.html',
            {
                'request': request,
                'detail': 'Usuário não encontrado.',
                'status': 'warning',
            },
        )
    if user.is_active:
        return templates.TemplateResponse(
            '/activation.html',
            {
                'request': request,
                'detail': 'Esta conta já foi verificada anteriormente.',
                'status': 'warning',
            },
        )
    user.is_active = True
    db.commit()

    return templates.TemplateResponse(
        '/activation.html',
        {
            'request': request,
            'detail': 'Conta ativada com sucesso! Você já pode fazer o login.',
            'status': 'sucess',
        },
    )
