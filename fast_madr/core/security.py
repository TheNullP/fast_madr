from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_madr.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    crypt_context,
    oauth2_scheme,
)
from fast_madr.core.database import Book, User, get_db
from fast_madr.schemas.user_schema import LoginModel, UserInfo, UserModel


class UserLogin:
    def __init__(self, db: Session):
        self.db = db

    def user_register(self, user: UserModel):

        db_user = User(
            username=user.username,
            email=user.email,
            password=crypt_context.hash(user.password)
        )

        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail='User or Email already exists.'
            )

    def user_login(self, user: LoginModel, exp: int = ACCESS_TOKEN_EXPIRE_MINUTES):
        user_on_db = self.db.query(User).filter_by(
            username=user.username).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=401,
                detail='Invalid Password or user.'
            )
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=401,
                detail='Invalid Password or user.'
            )

        exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=int(exp))
        payload = {
            'usr': user_on_db.username,
            'exp': exp,
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }

    def verify_token(self, access_token):
        try:
            token = jwt.decode(access_token, SECRET_KEY,
                               algorithms=[ALGORITHM])

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail='Expired Token Access.'
            )

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail='Invalid Access Token.'
            )
        except IntegrityError:
            raise HTTPException(
                status_code=401,
                detail='Invalid Access Token.'
            )

        user_on_db = self.db.query(User).filter_by(
            username=token['usr']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=401,
                detail='Invalid Access Token.'
            )
        return user_on_db

    def info_user(self, user_auth):

        user_db = self.db.query(User).filter_by(
            username=user_auth.username).first()
        name_created_books = self.db.query(
            Book).filter_by(id_user=user_db.id).all()
        created_books = len(name_created_books)

        if user_db.profile_picture is None:
            user_db.profile_picture = "/static/image/default.png"

        info = UserInfo(
            username=user_db.username,
            email=user_db.email,
            number_of_books=created_books,
            created_books=name_created_books,
            profile_picture=user_db.profile_picture,
        )

        return info


def token_verify(
    db_session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if token is None:
        raise HTTPException(
            status_code=401,
            detail='Token required.'
        )

    ul = UserLogin(db=db_session)
    user_data = ul.verify_token(access_token=token)

    if user_data is None:
        raise HTTPException(
            status_code=401,
            detail='Invalid or Expire Token.'
        )

    return user_data
