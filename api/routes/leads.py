from fastapi import APIRouter, HTTPException, BackgroundTasks
from ..models import GenerationRequest, GenerationResponse
from ..services.lead_service import LeadService
import uuid

router = APIRouter(prefix="/leads", tags=["leads"])
lead_service = LeadService()

@router.post("/generate", response_model=GenerationResponse)
async def generate_leads(
    request: GenerationRequest, 
    background_tasks: BackgroundTasks
):
    """Start lead generation process"""
    
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    task_id = str(uuid.uuid4())
    
    # Start background task
    background_tasks.add_task(
        lead_service.run_lead_generation, 
        task_id, 
        request.prompt
    )
    
    return GenerationResponse(
        task_id=task_id,
        status="queued",
        message="Lead generation started"
    )

@router.get("/export/{task_id}")
async def export_results(task_id: str, format: str = "json"):
    """Export task results"""
    return await lead_service.export_results(task_id, format)