from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'API для управления складом'
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
