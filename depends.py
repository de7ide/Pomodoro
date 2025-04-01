from fastapi import Depends

from database import get_db_session
from cache import get_redis_conn
from repository import TaskRepo, TaskCache
from services import TaskService


def get_tasks_repo() -> TaskRepo:
    db_session = get_db_session()
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