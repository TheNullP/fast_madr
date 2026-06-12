from datetime import datetime, timedelta
import smtplib
from zoneinfo import ZoneInfo

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from sib_api_v3_sdk.models.body import pprint
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
from fast_madr.core.settings import Settings
from fast_madr.schemas.user_schema import LoginModel, UserInfo, UserModel

import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

BREVO_KEY = Settings().BREVO_KEY


class UserLogin:
    def __init__(self, db: Session):
        self.db = db

    def user_register(self, user: UserModel):
        db_user = User(
            username=user.username,
            email=user.email,
            password=crypt_context.hash(user.password),
            is_active=False,
        )

        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)

        except IntegrityError:
            raise HTTPException(
                status_code=400, detail='User or Email already exists.'
            )

    def user_login(
        self, user: LoginModel, exp: int = ACCESS_TOKEN_EXPIRE_MINUTES
    ):
        user_on_db = (
            self.db.query(User).filter_by(username=user.username).first()
        )

        if user_on_db is None:
            raise HTTPException(
                status_code=401, detail='Invalid Password or user.'
            )
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=401, detail='Invalid Password or user.'
            )

        exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=int(exp))
        payload = {
            'usr': user_on_db.username,
            'exp': exp,
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {'access_token': access_token, 'token_type': 'bearer'}

    def verify_token(self, access_token):
        try:
            token = jwt.decode(
                access_token, SECRET_KEY, algorithms=[ALGORITHM]
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Expired Token Access.'
            )

        except JWTError:
            raise HTTPException(
                status_code=401, detail='Invalid Access Token.'
            )
        except IntegrityError:
            raise HTTPException(
                status_code=401, detail='Invalid Access Token.'
            )

        user_on_db = (
            self.db.query(User).filter_by(username=token['usr']).first()
        )

        if user_on_db is None:
            raise HTTPException(
                status_code=401, detail='Invalid Access Token.'
            )
        return user_on_db

    def info_user(self, user_auth):
        user_db = (
            self.db.query(User).filter_by(username=user_auth.username).first()
        )
        name_created_books = (
            self.db.query(Book).filter_by(id_user=user_db.id).all()
        )
        created_books = len(name_created_books)

        if user_db.profile_picture is None:
            user_db.profile_picture = '/static/image/default.png'

        info = UserInfo(
            username=user_db.username,
            email=user_db.email,
            number_of_books=created_books,
            created_books=name_created_books,
            profile_picture=user_db.profile_picture,
        )

        return info


def token_verify(
    db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    if token is None:
        raise HTTPException(status_code=401, detail='Token required.')

    ul = UserLogin(db=db_session)
    user_data = ul.verify_token(access_token=token)

    if user_data is None:
        raise HTTPException(status_code=401, detail='Invalid or Expire Token.')

    if not user_data.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Esta conta ainda não foi ativada. Verifique seu e-mail.',
        )

    return user_data


def create_activation_token(email: str):

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=15)
    payload = {
        'exp': expire,
        'sub': str(email),
        'scope': 'email_verification',
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {'access_token': access_token, 'token_type': 'bearer'}


def verify_activation_token(token: str):

    try:
        if token is None:
            raise HTTPException(status_code=401, detail='Token required')

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get('scope') != 'email_verification':
            return None
        return payload.get('sub')
    except JWTError:
        return None


async def send_activation_email(email: str, token: str):
    verification_url = f'http://madr-thenullp.duckdns.org/auth/verify-email?token={token["access_token"]}'

    html_template = (
        f"""<html> <head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Ative sua conta no MADR</title> </head> <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f6fa; color: #2c3e50;"> <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" max-width="600px" style="border-collapse: collapse; background-color: #ffffff; margin: 40px auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #e1e8ed;"> <tr> <td bgcolor="#2c3e50" align="center" style="padding: 30px 20px; border-top-left-radius: 12px; border-top-right-radius: 12px;"> <h1 style="color: #ffffff; margin: 0; font-size: 1.6rem; font-weight: 600; letter-spacing: -0.5px;"> 📚 Acervo de Livros MADR </h1> </td> </tr> <tr> <td style="padding: 40px 30px;"> <h2 style="color: #34495e; font-size: 1.4rem; margin-top: 0; font-weight: 600;">Olá!</h2> <p style="font-size: 1rem; line-height: 1.6; color: #4f5d73; margin-bottom: 30px;"> Seja muito bem-vindo ao nosso acervo. Para concluir o seu cadastro e liberar o seu acesso completo aos livros e downloads, precisamos apenas confirmar o seu endereço de e-mail. </p> <table align="center" border="0" cellpadding="0" cellspacing="0" style="margin: 30px auto;"> <tr> <td align="center" bgcolor="#3498db" style="border-radius: 8px;"><a href="{verification_url}" target="_blank" style="display: inline-block; padding: 14px 28px; font-size: 1rem; color: #ffffff; text-decoration: none; font-weight: 600; border-radius: 8px; transition: background-color 0.2s ease;"> Confirmar Meu E-mail </a> </td> </tr> </table> <p style="font-size: 0.9rem; line-height: 1.6; color: #7f8c8d; margin-top: 30px; text-align: center;"> Se o botão acima não funcionar, copie e cole o link abaixo no seu navegador: <br> <a href="{verification_url}" style="color: #3498db; word-break: break-all; font-size: 0.85rem;">{verification_url}</a> </p> </td> </tr> <tr> <td bgcolor="#f8f9fa" align="center" style="padding: 20px; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; border-top: 1px solid #e1e8ed;"> <p style="font-size: 0.8rem; color: #95a5a6; margin: 0;"> Este é um e-mail automático enviado pelo sistema fast_madr. Por favor, não responda a esta mensagem. </p> </td> </tr> </table> </body> </html>""",
    )

    sib_api_v3_sdk.configuration.Configuration().api_key['api-key'] = BREVO_KEY

    api_instance = sib_api_v3_sdk.EmailCampaignsApi()
    email_campaigns = sib_api_v3_sdk.CreateEmailCampaign(
        name='Campaign via the API',
        subject='TiTulo',
        sender={'name': 'MADR', 'email': 'thenullp00@gmail.com'},
        html_content=html_template,
    )
    try:
        api_response = api_instance.create_email_campaign(email_campaigns)
        pprint(api_response)
    except ApiException as e:
        print(
            'Exception when calling EmailCampaignsApi->create_email_campaign: %s\n',
            e,
        )
    except Exception as e:
        raise e
