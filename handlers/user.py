from typing import Annotated
from fastapi import APIRouter, Depends

from depends import get_user_service
from schemas import UserLoginSchema, UserCreateSchema
from services import UserService


router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(body.username, body.password)