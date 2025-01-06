from http import HTTPStatus
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fast_madr.models import User, get_db
from fast_madr.schema import UserModel
from fast_madr.security import UserLogin, token_verify
from fast_madr.security import oauth2_scheme, crypt_context


router = APIRouter()


@router.get("/users/", tags=["users"], status_code=HTTPStatus.OK)
def read_users(db: Session = Depends(get_db)):
    q = db.query(User).order_by(User.id).all()
    return q


@router.post("/user/", tags=["users"], status_code=HTTPStatus.CREATED)
def create_user(user: UserModel, db: Session = Depends(get_db)):
    ul = UserLogin(db=db)
    ul.user_register(user=user)

    return JSONResponse(
        content={'msg': 'success'},
        status_code=201,
    )


@router.put("/user/{user_id}", tags=["users"], status_code=HTTPStatus.OK)
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


@router.delete("/user/{user_id}", tags=["users"], status_code=HTTPStatus.OK)
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
