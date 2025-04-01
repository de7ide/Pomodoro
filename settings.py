from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_db: str = "pomodoro.sqlite"