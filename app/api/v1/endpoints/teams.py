from fastapi import APIRouter
from app.core.devops_service import get_devops_data

router = APIRouter()

@router.post("/request")
async def receive_teams_request():
    """Recebe requisição do Teams e busca dados no DevOps"""
    devops_data = get_devops_data()
    return {"message": "Dados recebidos do Azure Devops"}