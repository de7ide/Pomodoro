from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.depends import get_task_service, get_request_user_id
from app.exception import TaskNotFound
from app.tasks.schemas import TaskCreateSchema, TaskSchema
from app.tasks.service import TaskService


router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(
    task_services: Annotated[TaskService, Depends(get_task_service)]
):
    return await task_services.get_tasks()


@router.post("/create_task", response_model=TaskSchema)
async def task_app(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    task = await task_service.create_task(body, user_id)
    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def patch_task(task_id: int,
                     name: str,
                     task_service: Annotated[TaskService, Depends(get_task_service)],
                     user_id: int = Depends(get_request_user_id)):
    try:
        return await task_service.update_task_name(
            task_id=task_id,
            name=name,
            user_id=user_id
        )
    except TaskNotFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )


@router.delete("/del_task")
async def delete_task(task_id: int,
                      task_service: Annotated[TaskService, Depends(get_task_service)],
                      user_id: int = Depends(get_request_user_id)):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
