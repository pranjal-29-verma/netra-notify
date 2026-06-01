from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Gmail SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""   # Gmail App Password (not regular password)
    SMTP_FROM_NAME: str = "Netra"
    SMTP_ENABLED: bool = False  # set True in .env once App Password is ready

    # Frontend URL used inside email links
    FRONTEND_URL: str = "http://localhost:5173"

    # Shared secret — netra-app sends this in X-Api-Key header
    API_KEY: str = "change-me-in-production"

    # App
    PROJECT_NAME: str = "Netra Notify"
    VERSION: str = "1.0.0"

    model_config = ConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
