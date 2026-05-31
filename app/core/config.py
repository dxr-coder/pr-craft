from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str = ""
    base_url: str = "https://api.deepseek.com"

    model_config = {"env_file": ".env", "env_prefix": "DEEPSEEK_"}


settings = Settings()
