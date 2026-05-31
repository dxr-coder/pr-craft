from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    github_token: str = ""
    github_repo: str = "dxr-coder/pr-craft"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
