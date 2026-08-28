"""
Application configuration.

This module defines the application's configuration using
Pydantic Settings.

All environment variables should be accessed through the
Settings class rather than using os.getenv() directly.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings.

    Values are automatically loaded from the .env file.
    """

    app_name: str = "MRIP Backend"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    # ==========================
    # Database Configuration
    # ==========================

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # ==========================
    # JWT Configuration
    # ==========================

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==========================
    # Redis Configuration
    # ==========================

    redis_host: str = "localhost"
    redis_port: int = 6379

    
    @property
    def database_url(self) -> str:
        """
        Build the SQLAlchemy database URL.
        """

        return (
            f"postgresql+psycopg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )

    @property
    def redis_url(self) -> str:
        """
        Build the Redis URL.
        """

        return (
            f"redis://{self.redis_host}:{self.redis_port}/0"
        )
    
    @property
    def redis_url(self) -> str:
        """
        Build the Redis connection URL.
        """

        return f"redis://{self.redis_host}:{self.redis_port}/0"


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    The configuration is loaded only once during the
    application's lifetime.
    """
    return Settings()


settings = get_settings()