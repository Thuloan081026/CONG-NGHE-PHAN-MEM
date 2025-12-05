from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-to-a-secure-random-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str = "sqlite:///./database.db"


settings = Settings()
