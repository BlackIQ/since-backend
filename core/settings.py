# Libs
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_mode: str = ""

    # Database
    postgresql_url: str = ""

    # Security
    secret: str = ""
    algorithm: str = ""

    # Frontend
    frontend_url: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
