from pydantic_settings import BaseSettings
from pydantic import root_validator, field_validator, model_validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = None

    @model_validator(mode='before')
    @classmethod
    def generate_database_url(cls, values):
        db_url = f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        values['DATABASE_URL'] = db_url
        return values

    class Config:
        env_file = ".env"


settings = Settings()
