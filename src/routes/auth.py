from fastapi import APIRouter, Depends
from src.schemas.schemas import Login
from src.controllers.authentication_services import login_api, logout_api
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.middleware.islogin import oauth2_scheme

router = APIRouter(
    tags=[
        "Authentication",
    ]
)


@router.post("/login")
def login(creds: Login = Depends(), db: Session = Depends(get_db)):

    return login_api(
        email=creds.username, password=creds.password.get_secret_value(), db=db
    )


@router.get("/logout")
def logout(creds: dict = Depends(oauth2_scheme)):

    return logout_api(creds=creds)
