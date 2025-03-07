from fastapi import APIRouter
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
async def get_project_data(project_id: str):
    """Função que pega as infos do projeto"""
    project_status = get_project_status(project_id)
    overdue_tasks = get_overdue_tasks(project_id)
    work_hours = get_work_hours(project_id)

    return {
        "project_status": project_status,
        "overdue_tasks": overdue_tasks,
        "work_hours": work_hours
    }