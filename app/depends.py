from fastapi import Depends, HTTPException, Request, Security, security
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.auth.client.google import GoogleClient
from app.users.auth.client.yandex import YandexClient
from app.infrastucture.database import get_db_session
from app.infrastucture.cache import get_redis_conn
from app.exception import TokenExpire, TokenInvalide
from app.tasks.repository import TaskRepo, TaskCache
from app.users.user_profile.repository import UserRepo
from app.tasks.service import TaskService
from app.users.user_profile.service import UserService
from app.users.auth.service import AuthServices
from app.settings import Settings


async def get_tasks_repo(db_session: AsyncSession = Depends(get_db_session)) -> TaskRepo:
    return TaskRepo(db_session)


async def get_cache_tasks_repo() -> TaskCache:
    redis_conn = get_redis_conn()
    return TaskCache(redis_conn)


async def get_task_service(
        task_repo: TaskRepo = Depends(get_tasks_repo),
        task_cache: TaskCache = Depends(get_cache_tasks_repo)
) -> TaskService:
    return TaskService(
        task_repo=task_repo,
        task_cache=task_cache
    )


async def get_user_repo(db_session: AsyncSession = Depends(get_db_session)):
    return UserRepo(db_session=db_session)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> GoogleClient:
    return GoogleClient(settings=Settings())


async def get_yandex_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> YandexClient:
    return YandexClient(settings=Settings())


async def get_auth_service(
        user_repo: UserRepo = Depends(get_user_repo),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client)
) -> AuthServices:
    return AuthServices(
        user_repo=user_repo,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )


async def get_user_service(
    user_repo: UserRepo = Depends(get_user_repo),
    auth_service: AuthServices = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repo=user_repo, auth_service=auth_service)


reusable_auth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthServices = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_auth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenInvalide as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except TokenExpire as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    return user_id