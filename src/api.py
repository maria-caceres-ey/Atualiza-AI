# api.py
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_azure = "https://dev.azure.com/FSO-DnA-Devops/"
azure_token = os.getenv("AZURE_DEVOPS_TOKEN")

def get_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {azure_token}"
    }

def get_projects():
    url = f"{api_azure}_apis/projects?api-version=7.1"
    response = requests.get(url, headers=get_headers(), verify=False)
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        return []

def get_overdue_tasks(project_id):
    url = f"{api_azure}{project_id}/_apis/wit/wiql?api-version=7.1"
    body = {
        "query": "SELECT [System.Id], [System.Title], [System.AssignedTo], [System.State], [Microsoft.VSTS.Scheduling.TargetDate] "
                 "FROM WorkItems "
                 "WHERE [System.WorkItemType] = 'Task' AND [Microsoft.VSTS.Scheduling.TargetDate] < @Today AND [System.State] NOT IN ('Completed', 'Removed', 'Closed')"
    }
    response = requests.post(url, headers=get_headers(), json=body, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Erro ao se comunicar com o serviço. Código de status: {response.status_code}. Mensagem: {response.text}"}

def get_team(project_id):
    url = f"{api_azure}{project_id}/_apis/projects/{project_id}/teams?api-version=7.1"
    response = requests.get(url, headers=get_headers(), verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Erro ao se comunicar com o serviço. Código de status: {response.status_code}. Mensagem: {response.text}"}

def get_project_status(project_id):
    url = f"{api_azure}/status_do_projeto/{project_id}"  # Ajuste conforme necessário
    response = requests.get(url, headers=get_headers(), verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Erro ao se comunicar com o serviço. Código de status: {response.status_code}. Mensagem: {response.text}"}
