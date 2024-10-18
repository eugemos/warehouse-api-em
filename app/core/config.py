from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'API для управления складом'
    database_url: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
