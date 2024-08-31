import jwt
from typing import Optional
from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from starlette.requests import Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from src.database.connect import redis_client
from src.core.config import settings


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        cookie_authorization: str = request.cookies.get("Authorization")
        cookie_email: str = request.cookies.get("email")
        email, not_req = get_authorization_scheme_param(cookie_email)
        auth = get_authorization_scheme_param(cookie_authorization)
        if len(auth) > 2:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Authorization cookies must be a Bearer token",
                )
            else:
                return None
        cookie_scheme, cookie_param = auth
        if cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

            try:
                data = redis_client.get(param)
                email_redis = data.decode("utf-8")
                if email_redis != email:
                    raise HTTPException(
                        status_code=HTTP_403_FORBIDDEN, detail="Forbidden Access"
                    )
            except:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Token expired"
                )

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Authorization cookies must start with Bearer",
                )
            else:
                return None

        payload = jwt.decode(
            param, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        payload["token"] = param
        return payload


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/")
