import jwt
from passlib.context import CryptContext
from ..core.config import settings
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from src.schemas.schemas import CreateUser, UpdateUser
from src.database.models import User
from fastapi.responses import JSONResponse
from fastapi import status, UploadFile
from src.database.connect import s3_client


def hash_password(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def verify_password(hash_password: str, password: str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(password, hash_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_user_api(data: CreateUser, file: UploadFile, db: Session):
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/gif",
    ]

    try:
        user = db.query(User).filter(User.email == data.email).first()
        if user is None:

            if file.content_type not in allowed_types:
                return JSONResponse(
                    status_code=400,
                    content={
                        "message": "Invalid file type. Only image files (.jpeg, .png, .gif) are allowed."
                    },
                )
            file_data = file.file.read()
            temp_file_path = file.filename

            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file_data)

            # profile_url = ""
            password = hash_password(password=data.password.get_secret_value())
            s3_client.upload_file(
                temp_file_path,
                settings.AWS_S3_BUCKET,
                f"profile/{data.email}/{temp_file_path}",
            )
            new_user = User(
                email=data.email,
                first_name=data.first_name,
                last_name=data.last_name,
                profile=f"profile/{data.email}/{temp_file_path}",
                password=password,
                dob=data.dob,
            )

            db.add(new_user)
            db.commit()

            return JSONResponse(
                content={"message": f"User {data.email} register successfully"},
                status_code=status.HTTP_201_CREATED,
            )
        return JSONResponse(
            {"message": f"User {data.email} allready exsit"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"message": "Exception Ocuures"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_user_api(id: int, db: Session, user: str):
    try:
        if id is None:
            users = db.query(
                User.id,
                User.first_name,
                User.last_name,
                User.email,
                User.profile,
                User.dob,
                User.gender,
                User.is_active,
                User.created_at,
            ).all()
            user_data = []
            for user in users:

                user_data.append(
                    {
                        "id": str(user.id),
                        "first_name": str(user.first_name),
                        "last_name": str(user.last_name),
                        "email": str(user.email),
                        "profile": str(user.profile),
                        "dob": str(user.dob),
                        "gender": str(user.gender),
                        "is_active": str(user.is_active),
                        "created_at": str(user.created_at),
                    }
                )

            return JSONResponse(content=user_data, status_code=status.HTTP_200_OK)
        else:
            user = (
                db.query(
                    User.id,
                    User.first_name,
                    User.last_name,
                    User.email,
                    User.profile,
                    User.dob,
                    User.gender,
                    User.is_active,
                    User.created_at,
                )
                .filter(User.id == id)
                .first()
            )
            if user is None:

                return JSONResponse(
                    content={"message": "User dose not exsit"},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            user = {
                "id": str(user.id),
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "email": str(user.email),
                "gender": str(user.g),
                "profile": str(user.profile),
                "dob": str(user.dob),
                "gender": str(user.gender),
                "is_active": str(user.is_active),
                "created_at": str(user.created_at),
            }

        return JSONResponse(content=user, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"message": "Exception Ocurrs"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def delete_user_api(user_id: int, email: str, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return JSONResponse(
                content={"message": "User dose not exsit"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        db.delete(user)
        db.commit()
        return JSONResponse(
            content={"message": f"User {user.email} deleted"},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:

        print(e)
        return JSONResponse(
            content={"message": "Exception Ocuured"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def update_user_api(data: UpdateUser, email: str, db: Session):
    user = db.query(User).filter(User.id == data.id).update(data.__dict__)
    db.commit()
    # if user is None:

    #     return JSONResponse(
    #         content={"message": "User dose not exsit"},
    #         status_code=status.HTTP_404_NOT_FOUND,
    #     )

    # update_user = User(data.__dict__)
    # # print(data.__dict__)
    # db.commit()
    # db.refresh(update_user)
    return {}
