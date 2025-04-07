from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fast_madr.core.database import User, get_db
from fast_madr.schemas.user_schema import UserModel
from fast_madr.core.security import UserLogin, token_verify, crypt_context


router = APIRouter(prefix='/user')


@router.get("/search", tags=["user"], status_code=HTTPStatus.OK)
def read_users(db: Session = Depends(get_db)):
    q = db.query(User).order_by(User.id).all()
    return q


@router.post("/create", tags=["user"], status_code=HTTPStatus.CREATED)
def create_user(user: UserModel, db: Session = Depends(get_db)):
    ul = UserLogin(db=db)
    ul.user_register(user=user)

    return JSONResponse(
        content={'msg': 'success.'},
        status_code=201,
    )


@router.put("/update/", tags=["user"], status_code=HTTPStatus.OK)
def update_user(
    user: UserModel,
    db: Session = Depends(get_db),
    auth_user: User = Depends(token_verify),
):
    user_on_db = db.query(User).filter_by(username=user.username).first()
    if user_on_db:
        return JSONResponse(
            content={'msg': 'User already exists.'},
            status_code=400
        )
    else:
        user_update = db.query(User).filter_by(
            username=auth_user.username).first()
        user_update.username = user.username
        user_update.email = user.email
        user_update.password = crypt_context.hash(user.password)
        db.commit()

    return JSONResponse(
        content={'msg': 'success.'},
        status_code=200
    )


@router.delete("/delete", tags=["user"], status_code=HTTPStatus.OK)
def delete_user(
    db: Session = Depends(get_db),
    auth_user: User = Depends(token_verify),
):
    db.delete(auth_user)
    db.commit()
    return {"detail": "User deleted."}
