from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )


    # Application settings
    app_name: str = Field(
        default="GenAI",
        description="Application name"
    )
    app_version: str = Field(
        default="0.1.0",
        description="Application version"
    )


    # Logging settings
    debug: bool = Field(
        default=False,
        description="Debug mode"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    log_file: str = Field(
        default="logs/activity.log",
        description="Log file path"
    )
    backlog_date: int = Field(
        default=3,
        description="Days to backup log file"
    )


    # CORS settings
    cors_origins: List[str] = Field(
        default=["http://localhost:5000"],
        description="Allowed CORS origins (comma-separated string or list)"
    )


    # OpenAI settings
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="OpenAI API base URL"
    )
    openai_api_key: str = Field(
        default="",
        description="OpenAI API key"
    )


    # Prompt settings
    system_prompt_path: str = Field(
        default="prompts/system.yaml",
        description="Path to the system prompt YAML file"
    )


settings = Settings()

