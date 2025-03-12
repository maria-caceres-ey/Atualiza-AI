from fastapi import APIRouter
from app.api.v1.endpoints.devops import router as devops_router

router = APIRouter()

router.include_router(devops_router, prefix="/devops", tags=["Azure DevOps"])