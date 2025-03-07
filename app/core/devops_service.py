import requests
import os

AZURE_DEVOPS_URL = os.getenv("AZURE_DEVOPS_URL")
AZURE_DEVOPS_TOKEN = os.getenv("AZURE_DEVOPS_TOKEN")

def get_headers():
    return {

    }

def get_devops_data():
    url = f"{AZURE_DEVOPS_URL}/_apis/projects?api-version=6.0"
    response = requests.get(url, headers=get_headers())

    if response.status_code == 200:
        return response.json()
    return {"error": "Falha ao obter dados do Azure DevOps"}