from typing import Annotated

from fastapi import APIRouter, Depends

from depends import get_task_service, get_tasks_repo
from schemas.task import TaskSchema
from repository import TaskRepo
from services import TaskService



router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(
    task_services: Annotated[TaskService, Depends(get_task_service)]
):
    return task_services.get_tasks()



@router.post("/create_task", response_model=TaskSchema)
async def task_app(task: TaskSchema,
                   task_repo: Annotated[TaskRepo, Depends(get_tasks_repo)]):
    task_id = task_repo.create_task(task)
    task.id = task_id
    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def patch_task(task_id: int,
                     name: str,
                     task_repo: Annotated[TaskRepo, Depends(get_tasks_repo)]):
    return task_repo.update_name(task_id, name)

@router.delete("/del_task")
async def delete_task(task_id: int,
                      task_repo: Annotated[TaskRepo, Depends(get_tasks_repo)]):
    task_repo.delete_task(task_id)
    return {"message": "ZAEB"}
