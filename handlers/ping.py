from fastapi import APIRouter
from settings import Settings


router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/db")
async def ping_dp():
    settings = Settings()
    return {"message": settings.MY_FUCKING_ID}


@router.get("/app")
async def ping_app():
    return {"mess": "app workaet!"}