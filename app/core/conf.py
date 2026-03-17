import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Luna Organization API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@db:3306/db")
    STATIC_API_KEY: str = os.getenv("STATIC_API_KEY", "secret-token-777")

settings = Settings()