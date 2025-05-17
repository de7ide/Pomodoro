from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db_session
from cache import get_redis_conn
from repository import TaskRepo, TaskCache, UserRepo
from services import TaskService, UserService
from services import AuthServices


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
        task_repo=get_tasks_repo(),
        task_cache=get_cache_tasks_repo()
    )


def get_user_repo(db_session: Session = Depends(get_db_session)):
    return UserRepo(db_session=db_session)


def get_user_service(
        user_repo: UserRepo = Depends(get_user_repo)
) -> UserService:
    return UserService(user_repo=user_repo)


def get_auth_service(user_repo: UserRepo = Depends(get_user_repo)) -> AuthServices:
    return AuthServices(user_repo=user_repo)