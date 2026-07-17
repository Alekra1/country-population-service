from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    name: str = "postgres"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_")
