from fastapi import APIRouter, UploadFile, File, Depends
from src.controllers.user_services import (
    create_user_api,
    get_user_api,
    delete_user_api,
    update_user_api,
)
from src.database.connect import get_db
from sqlalchemy.orm import Session
from src.schemas.schemas import CreateUser, UpdateUser
from src.middleware.islogin import oauth2_scheme


router = APIRouter(
    tags=[
        "Users",
    ]
)


@router.get("/user")
def get_user(
    creds: dict = Depends(oauth2_scheme), id: int = None, db: Session = Depends(get_db)
):

    return get_user_api(id=id, db=db, user=creds["username"])


@router.post("/user")
def create_user(
    data: CreateUser = Depends(),
    profile: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    return create_user_api(data, profile, db)


@router.put("/edit-user")
def update_user(
    data: UpdateUser = Depends(),
    creds: dict = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    return update_user_api(data=data, email=creds["username"], db=db)


@router.delete("/delete-user")
def delete_user(
    id: int, creds: dict = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    return delete_user_api(user_id=id, email=creds["username"], db=db)
