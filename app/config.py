from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)
class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_name: str
    database_username: str
    database_password: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

# # Validate configuration
# if not SECRET_KEY:
#     raise ValueError("SECRET_KEY is missing or empty in .env")

# if not isinstance(SECRET_KEY, str):
#     raise TypeError("SECRET_KEY must be a string")

# print("SECRET_KEY loaded:", bool(SECRET_KEY))
# print("ALGORITHM:", ALGORITHM)
# print("TOKEN EXPIRY:", ACCESS_TOKEN_EXPIRE_MINUTES)