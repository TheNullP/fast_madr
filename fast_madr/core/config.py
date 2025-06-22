import cloudinary
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

from fast_madr.core.settings import Settings

ALGORITHM = Settings().ALGORITHM
SECRET_KEY = Settings().SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = Settings().ACCESS_TOKEN_EXPIRE_MINUTES
crypt_context = CryptContext(schemes=['sha256_crypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/token')
templates = Jinja2Templates(directory='fast_madr/templates')

# configura o Cloudinary
cloudinary.config(
    cloud_name=Settings().CLOUDINARY_CLOUD_NAME,
    api_key=int(Settings().CLOUDINARY_API_KEY),
    api_secret=Settings().CLOUDINARY_API_SECRET,
)
