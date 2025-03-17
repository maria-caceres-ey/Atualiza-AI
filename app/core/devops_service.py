import requests
import os
from datetime import datetime, timedelta

AZURE_DEVOPS_URL = os.getenv("AZURE_DEVOPS_URL")
AZURE_DEVOPS_TOKEN = os.getenv("AZURE_DEVOPS_TOKEN")

def get_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {AZURE_DEVOPS_TOKEN}",
    }

def get_projects():
    url = f"{AZURE_DEVOPS_URL}/_apis/projects?api-version=7.1" #OK
    response = requests.get(url, headers=get_headers())

    if response.status_code == 200:
        data = response.json()
        projects = [
            {
                "id": p["id"],
                "name": p["name"],
                "description":p.get("description", "Sem descrição"),
                "url": p["url"]
            }
            for p in data.get("value", [])
        ]
        return projects
    return {"error": "Falha ao obter dados do Azure DevOps"}

def select_project(project_id:str):
    url = f"{AZURE_DEVOPS_URL}/_apis/projects/{project_id}?api-version=7.1" #OK
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return {"error": "Falha ao obter dados do projeto {project_id}"}

def get_project_status(project_id:str):
    url = f"{AZURE_DEVOPS_URL}/{project_id}/_apis/wit/workitems?api-version=7.1"
    try:
       response = requests.get(url, headers=get_headers())
       response.raise_for_status()
         
       data = response.json()
       if "count" in data and data["count"] > 0:
           work_items = data["value"]
           status_count = {}

           for item in work_items:
               state = item["fields"].get("System.State", "Unknown")
               status_count[state] = status_count.get(state, 0) + 1
           print("Status do Projeto:")
           for state, count in status_count.items():
               print(f"{state}: {count} itens")
       else:
           print("Nenhum work item encontrado.")
    except requests.exceptions.RequestException as e:
       print(f"Erro ao consultar a API: {e}")

def get_overdue_tasks(project_id:str):
    url = f"{AZURE_DEVOPS_URL}/{project_id}/_apis/wit/workitems?api-version=7.1" #testando, ainda não está pegando as infos necessarias
   
    params = {
       "api-version": "7.1",
       "$filter": "Microsoft.VSTS.Scheduling.TargetDate lt '2025-03-13T00:00:00Z'" 
    }
    try:
       response = requests.get(url, headers=get_headers(), params=params)
       response.raise_for_status() 
       
       data = response.json()
       if "count" in data and data["count"] > 0:
           overdue_tasks = data["value"]
           print(f"Total de cards atrasados: {len(overdue_tasks)}")
           for task in overdue_tasks:
               title = task["fields"].get("System.Title", "Sem título")
               print(f"- {title}")
       else:
           print("Nenhum card atrasado encontrado.")
    except requests.exceptions.RequestException as e:
       print(f"Erro ao consultar a API: {e}")

def get_work_hours(project_id, period="weekly"):
    url = f"{AZURE_DEVOPS_URL}/{project_id}/_apis/wit/workitems?api-version=7.1" #testando, ainda não está pegando as infos necessarias
   
    today = datetime.today()
    if period == "weekly":
       start_date = today - timedelta(days=7)
    elif period == "monthly":
       start_date = today.replace(day=1)  
    else:
       raise ValueError("Período inválido. Use 'weekly' ou 'monthly'.")
   
    params = {
       "api-version": "7.1",
       "$filter": f"System.ChangedDate ge '{start_date.strftime('%Y-%m-%d')}T00:00:00Z'"
    }
    try:
       response = requests.get(url, headers=get_headers(), params=params)
       response.raise_for_status()  
       data = response.json()
       if "count" in data and data["count"] > 0:
           work_items = data["value"]
           total_completed = 0
           total_estimated = 0
           total_remaining = 0
        
           for item in work_items:
               fields = item.get("fields", {})
               total_completed += fields.get("Microsoft.VSTS.Scheduling.CompletedWork", 0)
               total_estimated += fields.get("Microsoft.VSTS.Scheduling.OriginalEstimate", 0)
               total_remaining += fields.get("Microsoft.VSTS.Scheduling.RemainingWork", 0)
           print(f"Período: {period.capitalize()}")
           print(f"- Horas Trabalhadas: {total_completed}h")
           print(f"- Horas Estimadas: {total_estimated}h")
           print(f"- Horas Restantes: {total_remaining}h")
       else:
           print("Nenhuma informação de horas encontrada no período.")
    except requests.exceptions.RequestException as e:
       print(f"Erro ao consultar a API: {e}")

def get_daily_tasks(project_id:str):
    url = f"{AZURE_DEVOPS_URL}/{project_id}/_apis/wit/workitems?api-version=7.1" #testando, ainda não está pegando as infos necessarias
   
    today = datetime.today().strftime('%Y-%m-%d')
   
    params = {
       "api-version": "7.1",
       "$filter": f"System.CreatedDate ge '{today}T00:00:00Z'"  
    }
    try:
       response = requests.get(url, headers=get_headers(), params=params)
       response.raise_for_status()  
       
       data = response.json()
       if "count" in data and data["count"] > 0:
           daily_tasks = data["value"]
           print(f"Total de atividades do dia: {len(daily_tasks)}")
           for task in daily_tasks:
               title = task["fields"].get("System.Title", "Sem título")
               print(f"- {title}")
       else:
           print("Nenhuma atividade registrada hoje.")
    except requests.exceptions.RequestException as e:
       print(f"Erro ao consultar a API: {e}")

def get_teams(project_id:str):
    url: f"{AZURE_DEVOPS_URL}/_apis/projects/{project_id}/teams?api-version=7.1"  #OK
    response = requests.post(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return {"error": f"Falha ao obter informações sobre a equipe do projeto {project_id}"}

def get_project_info(project_id:str, repository_id:str):
    project_status = get_project_status(project_id)
    overdue_tasks = get_overdue_tasks(project_id)
    work_hours = get_work_hours(project_id)
    daily_tasks = get_daily_tasks(project_id)
    team_info = get_teams(project_id)

    return{
        "project_status": project_status,
        "overdue_tasks": overdue_tasks,
        "work_hours": work_hours,
        "daily_tasks": daily_tasks,
        "team_info": team_info
    }