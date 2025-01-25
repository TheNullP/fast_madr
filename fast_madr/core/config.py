from decouple import config
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext




ALGORITHM=config('ALGORITHM')
SECRET_KEY=config('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES=config('ACCESS_TOKEN_EXPIRE_MINUTES')
crypt_context = CryptContext(schemes=['sha256_crypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/token')
templates = Jinja2Templates(directory='fast_madr/templates')
