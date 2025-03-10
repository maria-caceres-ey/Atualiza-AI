import requests
import os

AZURE_DEVOPS_URL = os.getenv("AZURE_DEVOPS_URL")
AZURE_DEVOPS_TOKEN = os.getenv("AZURE_DEVOPS_TOKEN")

def get_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {AZURE_DEVOPS_TOKEN}",
    }

def get_devops_data():
    url = f"{AZURE_DEVOPS_URL}/_apis/projects?api-version=6.0"
    response = requests.get(url, headers=get_headers())

    if response.status_code == 200:
        return response.json()
    return {"error": "Falha ao obter dados do Azure DevOps"}

def select_project(project_id:str):
    url = f"{AZURE_DEVOPS_URL}/_apis/projects/{project_id}?api-version=6.0"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return {"error": "Falha ao obter dados do projeto {project_id}"}

def get_project_status(project_id:str):
    url = f"{AZURE_DEVOPS_URL}/_apis/projects/{project_id}/state?api-version=6.0"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return {"error": "Falha ao obter dados do projeto {project_id}"}

def get_overdue_tasks(project_id:str):
    url = f"{AZURE_DEVOPS_URL}/_apis/wit/wiql?api-version=6.0"
    query = {
        "query": "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.State] = 'To Do' AND [System.CreatedDate] < @Today" 
    }
    response = requests.get(url,json=query, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return {"error": f"Falha ao obter tarefas atrasadas do projeto {project_id}"}

def get_work_hours(project_id:str):
    url = f"{AZURE_DEVOPS_URL}/_apis/git/repositories/{project_id}/commits?searchCriteria.itemVersion.versionType=commit&api-version=6.0"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        commits = response.json()
        total_hours = sum(commit.get("hours_spent", 0) for commit in commits)
        return {"total_hours": total_hours}
    return {"error": f"Falha ao obter as horas trabalhadas do projeto {project_id}"}

def get_daily_tasks(project_id:str):
    url: f"{AZURE_DEVOPS_URL};{project_id}/_apis/wit/wiql?api-version=6.0"
    query = {
        "query": "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.State] = 'In Progress' AND [System.CreatedDate] < @Today" 
    }
    response = requests.post(url, json=query, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return {"error": f"Falha ao obter tarefas diárias"}

def get_team(project_id:str):
    url: f"{AZURE_DEVOPS_URL};{project_id}/_apis/projects/{project_id}/teams?api-version=6.0"
    response = requests.post(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return {"error": f"Falha ao obter informações sobre a equipe do projeto {project_id}"}

def get_project_info(project_id:str):
    project_status = get_project_status(project_id)
    overdue_tasks = get_overdue_tasks(project_id)
    work_hours = get_work_hours(project_id)
    daily_tasks = get_daily_tasks(project_id)
    team_info = get_team(project_id)

    return{
        "project_status": project_status,
        "overdue_tasks": overdue_tasks,
        "work_hours": work_hours,
        "daily_tasks": daily_tasks,
        "team_info": team_info
    }
