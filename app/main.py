from fastapi import FastAPI
from app.tasks.handlers import router as tasks_routers
from app.users.auth.handlers import router as auth_routers
from app.users.user_profile.handlers import router as users_routers


app = FastAPI()

app.include_router(tasks_routers)
app.include_router(auth_routers)
app.include_router(users_routers)