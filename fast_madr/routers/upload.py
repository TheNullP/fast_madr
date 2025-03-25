from fastapi import APIRouter, Depends
from fastapi import File, UploadFile, HTTPException
from urllib.parse import urlparse
from sqlalchemy.orm import Session
import cloudinary.uploader
from fast_madr.core.config import cloudinary
from fast_madr.core.security import token_verify
from fast_madr.core.database import User, get_db


router = APIRouter()

MAX_FILE_SIZE =2 * 1024 * 1024 #2BM em bytes
ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/jpg"}


def get_public_id(image_url: str):

    parsed_url = urlparse(image_url)

    path = parsed_url.path

    path_parts = path.split("/")

    public_id = "/".join(path_parts[5:])

    public_id =  public_id.rsplit(".", 1)[0]

    return public_id

@router.post("/upload/profile-picture/")
async def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    auth_user: User = Depends(token_verify)
):


    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use JPEG ou PNG")

    file_size = await file.read()
    if len(file_size) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="O arquivo é muito grande. O limite é 2MB.")

    await file.seek(0)


    try: 
        # upload para o cloudinary
        public_id = get_public_id(auth_user.profile_picture)
        cloudinary.uploader.destroy(public_id)
        result = cloudinary.uploader.upload(file.file, folder="media/profile_pictures/")
        profile_url = result["secure_url"]

        # Atualiza o usuário com a nova foto
        auth_user.profile_picture = profile_url
        db.commit()
        db.refresh(auth_user)

        # retorn a URL da imagem armazenada
        return {"url": profile_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
