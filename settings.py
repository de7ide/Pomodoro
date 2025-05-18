from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_DRIVER: str = "postgresql+psycopg2"
    DB_USER: str = "admin"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "pomodoro"
    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = 'secretic))))'
    JWT_ENCODE_ALGO: str = 'HS256'

# postgresql+psycopg2://admin:password@localhost:5432/pomodoro
    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'