
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "FastAPI Auth Wrapper"
    
    # THE AUTHORIZATION SERVICE VARIABLES
    auth_service_url: str = Field(..., env="AUTH_SERVICE_URL")
    auth_service_token_url: str = Field(..., env="AUTH_SERVICE_TOKEN_URL")

def get_settings_dep():
    return Settings()


