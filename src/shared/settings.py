from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # This is in case we want to use a .env too, but environment vars are prioritized
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    api_v1_str: str = "/api/v1"
    backend_cors_origins: List[str] = [
        "http://localhost:5173",
    ]
    jwt_secret_key: str = "574387fbcb3fbf0c0e58c893f3a5fe40f6b244480137993adb8a1024f74ade5e"
    jwt_algorithm: str = "HS256"
    access_token_expire_seconds: int = 1800
    image_db_directory = "images/data/assets"
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_port: str
