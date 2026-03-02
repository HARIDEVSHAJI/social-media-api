from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # NEW (for Railway + production)
    DATABASE_URL: str | None = None

    # EXISTING (keep for now)
    database_hostname: str | None = None
    database_port: str | None = None
    database_password: str | None = None
    database_name: str | None = None
    database_username: str | None = None

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()