from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class GenerationRequest(BaseModel):
    prompt: str

class GenerationResponse(BaseModel):
    task_id: str
    status: str
    message: str

class GenerationResult(BaseModel):
    task_id: str
    status: str
    leads: Optional[List[Dict[str, Any]]] = None
    emails: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    created_at: datetime

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class Lead(BaseModel):
    company: str
    website: str
    description: str
    products: str
    match: str

class Email(BaseModel):
    company: str
    subject: str
    email: str