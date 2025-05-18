from dataclasses import dataclass
from exception import TaskNotFound
from repository import TaskRepo, TaskCache
from schemas import TaskCreateSchema, TaskSchema


@dataclass
class TaskService:
    task_repo: TaskRepo
    task_cache: TaskCache

    def get_tasks(self) -> list[TaskSchema]:
        if cache_task := self.task_cache.get_tasks():
            return cache_task
        else:
            tasks = self.task_repo.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema


    def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = self.task_repo.create_task(task=body, user_id=user_id)
        task = self.task_repo.get_task(task_id)
        return TaskSchema.model_validate(task)


    def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = self.task_repo.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFound
        task = self.task_repo.update_task_name(task_id=task_id, name=name)
        return TaskSchema.model_validate(task)


    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repo.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        task = self.task_repo.delete_task(task_id=task_id, user_id=user_id)
