from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_exp_minutes: int = 30
    refresh_token_exp_minutes: int = 60 * 24 * 7
    database_url: str = "sqlite:///./smartstore.db"
    cors_origins: list[str] = ["http://localhost:5173"]
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    low_stock_check_hour_utc: int = 1


settings = Settings()
