from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_madr.models import User, get_db
from fast_madr.security import create_access_token, verify_password

router = APIRouter()


@router.post("/token",  tags=['token'])
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")


    access_token = create_access_token(data={'sub': user.email})

    return{'access_token': access_token, 'token_type': 'bearer'}
