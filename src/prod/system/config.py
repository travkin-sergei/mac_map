from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv("test.env"))


class Settings(BaseSettings):
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(case_sensitive=False)


settings = Settings()
