from http import HTTPStatus
from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from fast_madr.models import User, get_db
from fast_madr.schema import UserInfo, UserModel
from fast_madr.security import UserLogin, token_verify
from fast_madr.security import crypt_context



router = APIRouter(prefix='/user')


@router.get("/search", tags=["user"], status_code=HTTPStatus.OK)
def read_users(db: Session = Depends(get_db)):
    q = db.query(User).order_by(User.id).all()
    return q


@router.post("/register", tags=["user"], status_code=HTTPStatus.CREATED)
def create_user(user: UserModel, db: Session = Depends(get_db)):
    ul = UserLogin(db=db)
    ul.user_register(user=user)

    return JSONResponse(
        content={'msg': 'success'},
        status_code=201,
    )


@router.put("/update/{user_id}", tags=["user"], status_code=HTTPStatus.OK)
def update_user(
    user_id: int,
    user: UserModel,
    db: Session = Depends(get_db),
    token: User = Depends(token_verify),
):
    up_user = db.get(User, user_id)
    if not up_user:
        raise HTTPException(status_code=404, detail="User not found.")
    else:
        up_user.username = user.username
        up_user.email = user.email
        up_user.password = crypt_context.hash(user.password)
    db.commit()
    db.refresh(up_user)

    return {
        "id": user_id,
        "username": user.username,
        "email": user.email,
    }


@router.delete("/delete/{user_id}", tags=["user"], status_code=HTTPStatus.OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: User = Depends(token_verify),
):
    existing_user = db.get(User, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(existing_user)
    db.commit()
    return {"detail": "User deleted."}


@router.get('/profile', response_class=HTMLResponse)
async def get_profile():
    with open('fast_madr/templates/profile.html') as file:
        html = file.read()
        return HTMLResponse(content=html, status_code=200)

@router.get('/info_user')
def get_user_infor(
    user: User = Depends(token_verify),
    db: Session = Depends(get_db),
):
    ul  = UserLogin(db=db)
    infor_user = ul.info_user(user_auth=user)

    infor_user = UserInfo(
        username=infor_user.username,
        email=infor_user.email
    )

    return infor_user


