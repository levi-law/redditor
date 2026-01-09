"""Configuration management for Redditor.

Uses Pydantic Settings for environment variable management
with validation and type hints.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedditSettings(BaseSettings):
    """Reddit API configuration."""
    
    client_id: str = Field(default="", description="Reddit OAuth2 client ID")
    client_secret: str = Field(default="", description="Reddit OAuth2 client secret")
    user_agent: str = Field(default="redditor/0.1.0", description="Reddit API user agent")
    username: Optional[str] = Field(default=None, description="Reddit username (optional)")
    password: Optional[str] = Field(default=None, description="Reddit password (optional)")
    
    model_config = SettingsConfigDict(
        env_prefix="REDDIT_",
        env_file=".env",
    )


class AISettings(BaseSettings):
    """AI API configuration."""
    
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    
    model_config = SettingsConfigDict(
        env_file=".env",
    )


class DatabaseSettings(BaseSettings):
    """Database configuration."""
    
    url: str = Field(
        default="sqlite:///./redditor.db",
        description="Database connection URL",
    )
    echo: bool = Field(default=False, description="Echo SQL queries")
    
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file=".env",
    )


class Settings(BaseSettings):
    """Main application settings combining all sub-settings."""
    
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Sub-settings
    reddit: RedditSettings = Field(default_factory=RedditSettings)
    ai: AISettings = Field(default_factory=AISettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    model_config = SettingsConfigDict(
        env_prefix="REDDITOR_",
        env_file=".env",
    )
    
    def is_reddit_configured(self) -> bool:
        """Check if Reddit credentials are configured."""
        return bool(self.reddit.client_id and self.reddit.client_secret)
    
    def is_ai_configured(self) -> bool:
        """Check if AI API keys are configured."""
        return bool(self.ai.openai_api_key or self.ai.anthropic_api_key)


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
