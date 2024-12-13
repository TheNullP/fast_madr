from http import HTTPStatus
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from fast_madr.models import User, get_db
from fast_madr.schema import UserModel
from fast_madr.security import get_password_hash
from fast_madr.security import oauth2_scheme


router = APIRouter()


@router.get("/users/", tags=["users"], status_code=HTTPStatus.OK)
def read_users(db: Session = Depends(get_db)):
    q = db.query(User).order_by(User.id).all()
    return q


@router.post("/user/", tags=["users"], status_code=HTTPStatus.CREATED)
def create_user(user: UserModel, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter((User.email == user.email or User.username == user.username))
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")
    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": user.username, "email": user.email}


@router.put("/user/{user_id}", tags=["users"], status_code=HTTPStatus.OK)
def update_user(token: Annotated[str, Depends(oauth2_scheme)], user_id: int, user: UserModel, db: Session = Depends(get_db)):
    up_user = db.get(User, user_id)
    if not up_user:
        raise HTTPException(status_code=404, detail="User not found.")
    else:
        up_user.username = user.username
        up_user.email = user.email
        up_user.password = get_password_hash(user.password)
    db.commit()
    db.refresh(up_user)

    return {
        "id": user_id,
        "username": user.username,
        "email": user.email,
    }


@router.delete("/user/{user_id}", tags=["users"], status_code=HTTPStatus.OK)
def delete_user(token: Annotated[str, Depends(oauth2_scheme)], user_id: int, db: Session = Depends(get_db)):
    existing_user = db.get(User, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(existing_user)
    db.commit()
    return {"detail": "User deleted."}
