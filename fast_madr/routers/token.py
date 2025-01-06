from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fast_madr.schema import LoginModel
from fast_madr.security import UserLogin, oauth2_scheme, token_verify
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_madr.models import User, get_db

router = APIRouter()


@router.post('/user/token', tags=['token'])
def user_login(
    form_access: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = LoginModel(
        username=form_access.username,
        password=form_access.password
    )

    ul = UserLogin(db=db)
    data = ul.user_login(user=user)

    return data


@router.get('/test', tags=['token'])
def  test_access(
    token: User = Depends(token_verify)
):
    return 'Its Works.'
