from fastapi import APIRouter, Depends
from fastapi import File, UploadFile, HTTPException
import cloudinary.uploader
from sqlalchemy.orm import Session
from fast_madr.core.config import cloudinary
from fast_madr.core.security import token_verify
from fast_madr.core.database import User, get_db


router = APIRouter()

MAX_FILE_SIZE =2 * 1024 * 1024 #2BM em bytes
ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/jpg"}

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
