from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class AppConfig(BaseSettings):
    
    username: str | None = None
    password: str | None = None
    
    IMAGE_DIR: str
    LOG_DIR: Path
    
    WEB_SERVER_WORKERS: int
    WEB_SERVER_START_PORT: int

    POSTGRES_DB: str
    POSTGRES_DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str

    PGBOUNCER_USER: str
    PGBOUNCER_PASSWORD: str
    PGBOUNCER_HOST: str
    PGBOUNCER_PORT: int
    USE_PGBOUNCER: bool = True
    
    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    SUPPORTED_FORMATS: set[str] = {'.jpg', '.png', '.gif'}
    
    model_config = SettingsConfigDict(
        env_file = str(BASE_DIR / ".env"),
        enable_decoding = "utf-8",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def pgbouncer_url(self) -> str:
        return (
            f"postgresql://{self.PGBOUNCER_USER}:{self.PGBOUNCER_PASSWORD}@"
            f"{self.PGBOUNCER_HOST}:{self.PGBOUNCER_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def db_url(self) -> str:
        return self.pgbouncer_url if self.USE_PGBOUNCER else self.database_url

    
config = AppConfig()
    