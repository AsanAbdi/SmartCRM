from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "smartCrmDb"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key"
    MAX_LIMIT: int = 200
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES : int = 150
    SUPERUSER_USERNAME: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_EMAIL: EmailStr
    SUPERUSER_ROLE: str
    NORMAL_USER_USERNAME: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
