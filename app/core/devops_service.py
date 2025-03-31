import requests
import os
from datetime import datetime, timedelta
import json

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
    url = f"{AZURE_DEVOPS_URL}/{project_id}/_apis/wit/wiql?api-version=7.1"

    today = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    wiql_query = {
    "query": f"""
    SELECT [System.Id], [System.Title], [System.AssignedTo], [System.State], [Microsoft.VSTS.Scheduling.TargetDate] 
    FROM WorkItems 
    WHERE [System.WorkItemType] = 'Task' 
    AND [Microsoft.VSTS.Scheduling.TargetDate] < '{today}'
    AND [System.State] NOT IN ('Completed', 'Removed', 'Closed')
    """
    }

    try:
        response = requests.post(url, headers= get_headers(), data=json.dumps(wiql_query))
        response.raise_for_status()

        data = response.json()

        if "workItems" in data and len(data["workItems"]) > 0:
            work_items = data["workItems"]
            print(f"Total de cards atrasados: {len(work_items)}")
            for item in work_items:
                work_item_id = item["id"]

                details_url = f"https://dev.azure.com/{AZURE_DEVOPS_URL}/{project_id}/_apis/wit/workitems/{work_item_id}?api-version=7.1"
                details_response = requests.get(details_url, headers=get_headers())
                details_response.raise_for_status()
                work_item_data = details_response.json()

                title = work_item_data["fields"].get("System.Title", "Sem título")
                assigned_to = work_item_data["fields"].get("System.AssignedTo", {}).get("displayName", "Não atribuído")
                target_date = work_item_data["fields"].get("Microsoft.VSTS.Scheduling.TargetDate", "Data não disponível")

                print(f"- {title} (Atribuído a: {assigned_to}, Target Date: {target_date})")

        else:

            print("Nenhum card atrasado encontrado.")

    except requests.exceptions.RequestException as e:

        print(f"Erro ao consultar a API: {e}") 

def get_work_hours(project_id):
    url = f"{AZURE_DEVOPS_URL}/{project_id}/_apis/wit/wiql?api-version=7.1" 
    wiql_query = {
        "query": """
        SELECT [System.Id], [System.Title], [System.AssignedTo], [Microsoft.VSTS.Scheduling.CompletedWork]
        FROM WorkItems
        WHERE [System.WorkItemType] = 'Task'
        AND [Microsoft.VSTS.Scheduling.CompletedWork] > 0
        """
    }
    try:
        print("Enviando consulta WIQL para obter horas trabalhadas...")
        response = requests.post(url, headers=get_headers(), data=json.dumps(wiql_query))
        print("Resposta da requisição WIQL:", response.status_code)
        
        if response.status_code != 200:
            print("Erro na requisição:", response.text)
            return
        data = response.json()
        print("Dados retornados pela API:", json.dumps(data, indent=4))
        
        if "workItems" in data and len(data["workItems"]) > 0:
            work_items = data["workItems"]
            work_hours_per_person = {}
            for item in work_items:
                work_item_id = item["id"]
                details_url = f"{AZURE_DEVOPS_URL}/{project_id}/_apis/wit/workitems/{work_item_id}?api-version=7.1"
                details_response = requests.get(details_url, headers=get_headers())
            
                if details_response.status_code != 200:
                    print(f"Erro ao obter detalhes do WorkItem {work_item_id}: {details_response.text}")
                    continue
                work_item_data = details_response.json()
        
                title = work_item_data["fields"].get("System.Title", "Sem título")
                assigned_to = work_item_data["fields"].get("System.AssignedTo", {}).get("displayName", "Não atribuído")
                completed_work = work_item_data["fields"].get("Microsoft.VSTS.Scheduling.CompletedWork", 0)
            
                if assigned_to not in work_hours_per_person:
                    work_hours_per_person[assigned_to] = 0
                work_hours_per_person[assigned_to] += completed_work
                print(f"- {title}: {completed_work} horas (Atribuído a: {assigned_to})")
        
            print("\nHoras trabalhadas por pessoa no projeto:")
            for person, hours in work_hours_per_person.items():
                print(f"- {person}: {hours} horas")
        else:
            print("Nenhuma tarefa com horas trabalhadas encontrada.")
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