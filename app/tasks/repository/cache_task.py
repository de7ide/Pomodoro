from redis import asyncio as Redis
import json
from app.tasks.schemas import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TaskSchema]:
        tasks_json = self.redis.lrange("tasks", 0, -1)
        return [TaskSchema.model_validate(json.loads(task)) for task in tasks_json]


    async def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = [task.json() for task in tasks]
        if tasks_json:
            await self.redis.lpush("tasks", *tasks_json)