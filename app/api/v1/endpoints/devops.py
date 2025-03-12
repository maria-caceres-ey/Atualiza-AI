from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.core.devops_service import (
   get_projects, 
   select_project, 
   get_project_status,
   get_overdue_tasks, 
   get_work_hours, 
   get_daily_tasks, 
   get_teams, 
   get_project_info
)

router = APIRouter()

@router.get("/projects", response_model=List[Dict[str, Any]])
async def list_projects():
   projects = get_projects()
   if "error" in projects:
       raise HTTPException(status_code=500, detail=projects["error"])
   return projects

@router.get("/projects/{project_id}", response_model=Dict[str, Any])
async def project_details(project_id: str):
   project = select_project(project_id)
   if "error" in project:
       raise HTTPException(status_code=404, detail=project["error"])
   return project

@router.get("/projects/{project_id}/status", response_model=Dict[str, Any])
async def project_status(project_id: str):
   status = get_project_status(project_id)
   if "error" in status:
       raise HTTPException(status_code=500, detail=status["error"])
   return status

@router.post("/projects/{project_id}/overdue_tasks", response_model=Dict[str, Any])
async def overdue_tasks(project_id: str):
   tasks = get_overdue_tasks(project_id)
   if "error" in tasks:
       raise HTTPException(status_code=500, detail=tasks["error"])
   return tasks

@router.post("/projects/{project_id}/work_hours/{repository_id}", response_model=Dict[str, Any])
async def work_hours(project_id: str, repository_id: str):
   hours = get_work_hours(project_id, repository_id)
   if "error" in hours:
       raise HTTPException(status_code=500, detail=hours["error"])
   return hours

@router.post("/projects/{project_id}/daily_tasks", response_model=Dict[str, Any])
async def daily_tasks(project_id: str):
   tasks = get_daily_tasks(project_id)
   if "error" in tasks:
       raise HTTPException(status_code=500, detail=tasks["error"])
   return tasks

@router.get("/projects/{project_id}/team", response_model=Dict[str, Any])
async def project_team(project_id: str):
   team_info = get_teams(project_id)
   if "error" in team_info:
       raise HTTPException(status_code=500, detail=team_info["error"])
   return team_info

@router.get("/project_info/{project_id}/{repository_id}", response_model=Dict[str, Any])
async def project_info(project_id: str, repository_id: str):
   info = get_project_info(project_id, repository_id)
   if "error" in info:
       raise HTTPException(status_code=500, detail=info["error"])
   return info