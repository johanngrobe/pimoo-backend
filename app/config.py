from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Project Settings
    PROJECT_NAME: str

    # Database Settings
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str

    # User Settings
    JWT_SECRET_KEY: str
    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str
    JWT_LIFETIME_SECONDS: int

    # FastAPI Settings
    ALLOW_ORIGINS: List[str]
    ROOT_PATH: str
    VITE_FRONTEND_URL: str
    VITE_BACKEND_URL: str
    DOMAIN: str

    # Mail Settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool


settings = Settings()
