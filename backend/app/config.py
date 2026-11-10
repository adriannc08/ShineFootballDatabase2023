from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://fdi:fdi_local_dev@localhost:5432/fdi"
    apisports_key: str = ""
    apisports_base_url: str = "https://v3.football.api-sports.io"
    initial_season: int = 2023
    country: str = "Spain"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
