from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://salespulse:salespulse_dev_password@localhost:5432/salespulse"
    log_level: str = "INFO"
    raw_dir: Path = Path("data/raw")
    processed_dir: Path = Path("data/processed")
    quarantine_dir: Path = Path("data/quarantine")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
