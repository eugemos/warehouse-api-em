from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'API для управления складом'

    class Config:
        env_file = '.env'


settings = Settings()
