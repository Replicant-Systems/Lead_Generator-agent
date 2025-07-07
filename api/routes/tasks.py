from fastapi import APIRouter, HTTPException
from ..models import TaskStatus
from ..services.lead_service import LeadService

router = APIRouter(prefix="/tasks", tags=["tasks"])
lead_service = LeadService()

@router.get("/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """Get task status and results"""
    return await lead_service.get_task_status(task_id)

@router.get("/")
async def get_all_tasks():
    """Get all tasks (for debugging)"""
    return await lead_service.get_all_tasks()

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    return await lead_service.delete_task(task_id)