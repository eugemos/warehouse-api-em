from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения"""
    app_title: str = 'API для управления складом'
    test_mode: bool = False
    # db_type: DBType = DBType.SQLITE
    sqlite_db: str = ''
    postgres_db: str = 'warehouse'
    postgres_user: str = 'warehouse-api'
    postgres_password: str = 'password'
    db_host: str = 'db'
    db_port: int = 5432

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def database_url(self) -> str:
        if self.test_mode:
            return 'sqlite+aiosqlite:///:memory:'

        if self.sqlite_db:
            return f'sqlite+aiosqlite:///{self.sqlite_db}'

        return (
            'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}@'
            f'{self.db_host}:{self.db_port}/{self.postgres_db}'
        )


settings = Settings()
