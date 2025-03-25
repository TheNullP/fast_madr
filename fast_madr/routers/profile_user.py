from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from fast_madr.core.database import User, get_db
from fast_madr.core.security import UserLogin, token_verify
from fast_madr.core.config import templates

router = APIRouter(prefix='/user')

@router.get('/login', tags=['profile'], response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse('/auth/login.html', {'request': request, 'title': 'page test'})

@router.get('/profile',tags=['profile'], response_class=HTMLResponse)
async def get_profile(request: Request):
    return templates.TemplateResponse('/auth/profile.html', {'request': request, 'title': 'page'})

@router.get('/register', tags=['profile'], response_class=HTMLResponse)
async def get_create_user(request: Request):
    return templates.TemplateResponse('/auth/register.html', {'request': request, 'title': 'create user'})


@router.get('/info_user', tags=['profile'])
def get_user_infor(
    user: User = Depends(token_verify),
    db: Session = Depends(get_db),
):
    ul  = UserLogin(db=db)
    infor_user = ul.info_user(user_auth=user)

    return infor_user
