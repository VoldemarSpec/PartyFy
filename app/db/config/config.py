from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class DBSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}" \
               f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    class Config:
        env_file = ".env"

db_settings = DBSettings()
