from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from fast_madr.models import User, get_db
from fast_madr.schema import UserInfo
from fast_madr.security import UserLogin, token_verify, templates

router = APIRouter(prefix='/user')

@router.get('/login', tags=['profile'], response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse('/auth/login.html', {'request': request, 'title': 'page test'})

@router.get('/profile',tags=['profile'], response_class=HTMLResponse)
async def get_profile(request: Request):
    return templates.TemplateResponse('/auth/profile.html', {'request': request, 'title': 'page'})


@router.get('/info_user', tags=['profile'])
def get_user_infor(
    user: User = Depends(token_verify),
    db: Session = Depends(get_db),
):
    ul  = UserLogin(db=db)
    infor_user = ul.info_user(user_auth=user)

    infor_user = UserInfo(
        username=infor_user.username,
        email=infor_user.email,
    )

    return infor_user

