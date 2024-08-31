from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=[
        "Home",
    ]
)


@router.get("/")
def home():

    return JSONResponse(
        content={"message": "Initial route"}, status_code=status.HTTP_200_OK
    )
