from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql+psycopg2://admin:password@localhost:5432/pomodoro")


Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session


import sqlite3
from settings import Settings


settings = Settings()


def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect(settings.sqlite_db)