from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    AZURE_DEVOPS_URL = os.getenv("AZURE_DEVOPS_URL")
    AZURE_DEVOPS_TOKEN = os.getenv("AZURE_DEVOPS_TOKEN")
    API_KEY = os.getenv("API_KEY")
    API_ENDPOINT = os.getenv("API_ENDPOINT")
    API_EXPIRES_DATE = os.getenv("API_EXPIRES_DATE")

settings = Settings()