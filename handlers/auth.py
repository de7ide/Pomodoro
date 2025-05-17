from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from depends import get_auth_service
from exception import UserNotFoundException, UserNotFoundPasswordException
from schemas import UserLoginSchema, UserCreateSchema
from services import AuthServices



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/login",
    response_model=UserLoginSchema
)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthServices, Depends(get_auth_service)]
):
    try:
        user_login_data = auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserNotFoundPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return auth_service.login(body.username, body.password)