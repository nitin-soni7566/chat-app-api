from src.controllers.user_services import verify_password, create_access_token
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.connect import redis_client
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import timedelta
from src.core.config import settings
from redis.exceptions import RedisError


def login_api(email: str, password: str, db: Session):
    try:
        user = db.query(User).filter(User.email == email).first()

        if user is None:

            return JSONResponse(
                content={"message": "User does'not exsit"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if verify_password(hash_password=user.password, password=password):
            pass
        else:

            return JSONResponse(
                content={"message": "Invalid username password"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = create_access_token(
            {
                "id": user.id,
                "username": user.email,
            }
        )

        try:
            redis_client.set(access_token, email)
            redis_client.expire(
                access_token, timedelta(seconds=settings.REDIS_EXP_TIME)
            )
        except RedisError as err:
            print(err)
            return JSONResponse(
                content={"message": "Exception in redis"}, status_code=500
            )
        response = JSONResponse(
            content={"token": access_token, "token_type": "Bearer"},
            status_code=status.HTTP_200_OK,
        )
        response.set_cookie("Authorization", f"Bearer {access_token}", httponly=True)
        response.set_cookie("email", f"{email}", httponly=True)

        return response
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"message": "Exception Occurred"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def logout_api(creds):
    try:
        print(creds)
        redis_client.delete(creds["token"])
        return JSONResponse(
            content={"message": "logout successfully"}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"message": "Exception Occurred"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
