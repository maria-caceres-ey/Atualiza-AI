from fastapi import APIRouter
from app.api.v1.endpoints import devops, teams

router = APIRouter()

router.include_router(devops.router, prefix="/devops", tags=["Azure DevOps"])
router.include_router(teams.router, prefix="/teams", tags=["Teams"])