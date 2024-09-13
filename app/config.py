from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ENCODING_ALG: str
    REDIS_HOST: str
    REDIS_PORT: int
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    JWT_TOKEN_ACCESS_EXPIRE_M: int

    class Config:
        env_file = ".env"


settings = Settings()
