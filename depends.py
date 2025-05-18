from fastapi import Depends, HTTPException, Request, Security, security
from sqlalchemy.orm import Session

from database import get_db_session
from cache import get_redis_conn
from exception import TokenExpire, TokenInvalide
from repository import TaskRepo, TaskCache, UserRepo
from services import TaskService, UserService
from services import AuthServices
from settings import Settings


def get_tasks_repo(db_session: Session = Depends(get_db_session)) -> TaskRepo:
    return TaskRepo(db_session)


def get_cache_tasks_repo() -> TaskCache:
    redis_conn = get_redis_conn()
    return TaskCache(redis_conn)


def get_task_service(
        task_repo: TaskRepo = Depends(get_tasks_repo),
        task_cache: TaskCache = Depends(get_cache_tasks_repo)
) -> TaskService:
    return TaskService(
        task_repo=task_repo,
        task_cache=task_cache
    )


def get_user_repo(db_session: Session = Depends(get_db_session)):
    return UserRepo(db_session=db_session)


def get_auth_service(user_repo: UserRepo = Depends(get_user_repo)) -> AuthServices:
    return AuthServices(user_repo=user_repo, settings=Settings())


def get_user_service(
    user_repo: UserRepo = Depends(get_user_repo),
    auth_service: AuthServices = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repo=user_repo, auth_service=auth_service)


reusable_auth2 = security.HTTPBearer()


def get_request_user_id(
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