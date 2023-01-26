# Stdlib Imports
from pydantic import BaseSettings
from functools import lru_cache

# Third Party Imports
from decouple import config as environ


class Settings(BaseSettings):
    """Settings to hold environmental variables."""

    VOYAGE_API_KEY: str = environ("VOYAGE_API_KEY", cast=str)
    VOYAGE_SECRET_KEY: str = environ("VOYAGE_SECRET_KEY", cast=str)


@lru_cache
def get_setting_values() -> Settings:
    return Settings()
