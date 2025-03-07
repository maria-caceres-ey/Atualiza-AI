from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    AZURE_DEVOPS_URL: str = os.getenv("AZURE_DEVOPS_URL")
    AZURE_DEVOPS_TOKEN: str = os.getenv("AZURE_DEVOPS_TOKEN")

settings = Settings()