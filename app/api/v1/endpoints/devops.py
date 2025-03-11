from fastapi import APIRouter, HTTPException
from app.core.teams_service import send_teams_message
from app.core.devops_service import (
    select_project,
    get_project_status,
    get_overdue_tasks,
    get_work_hours,
    get_daily_tasks,
    get_team,
    get_project_info
)

router = APIRouter()

@router.get("/project/{project_id}")
async def get_project_info_endpoint(project_id:str):
    project_data = get_project_info(project_id)
    if "error" in project_data:
        raise HTTPException(status_code=400, detail=project_data["error"])
    return project_data

@router.get("/projects/{project_id}/status")
async def get_project_status_endpoint(project_id:str):
    status = get_project_status(project_id)
    if "error" in status:
        raise HTTPException(status_code=400, detail=status["error"])
    return status

@router.get("/projects/{project_id}/overdue-tasks")
async def get_overdue_tasks_endpoint(project_id: str):
    overdue_tasks = get_overdue_tasks(project_id)
    if "error" in overdue_tasks:
        raise HTTPException(status_code=400, detail=overdue_tasks["error"])
    return overdue_tasks

@router.get("/projects/{project_id}/work-hours")
async def get_work_hours_endpoint(project_id: str):
    work_hours = get_work_hours(project_id)
    if "error" in work_hours:
        raise HTTPException(status_code=400, detail=work_hours["error"])
    return work_hours

@router.get("/projects/{project_id}/daily-tasks")
async def get_daily_tasks_endpoint(project_id: str):
    daily_tasks = get_daily_tasks(project_id)
    if "error" in daily_tasks:
        raise HTTPException(status_code=400, detail=daily_tasks["error"])
    return daily_tasks

@router.get("/projects/{project_id}/team")
async def get_team_endpoint(project_id: str):
    team_info = get_team(project_id)
    if "error" in team_info:
        raise HTTPException(status_code=400, detail=team_info["error"])
    return team_info

@router.get("/notify_teams/{project_id}")
async def notify_teams(project_id: str):
    project_info = get_project_info(project_id)

    if "error" in project_info:
        return project_info
    
    message = f"Status do projeto {project_id}: {project_info['state']}"
    send_teams_message(message)

    return {"message": "Notificação enviada com sucesso"}