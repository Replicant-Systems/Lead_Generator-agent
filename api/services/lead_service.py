import asyncio
import os
from datetime import datetime
from typing import Dict, Any
from fastapi import HTTPException

# Import your existing orchestrator
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.orchestrator import LeadGenOrchestrator

class LeadService:
    def __init__(self):
        self.generation_tasks = {}
        self.mock_data = self._get_mock_data()
    
    def _get_mock_data(self):
        """Mock data for development"""
        return {
            "leads": [
                {
                    "company": "Texas Instruments",
                    "website": "ti.com",
                    "description": "Leading semiconductor manufacturer with global operations",
                    "products": "Microcontrollers, processors, analog chips",
                    "match": "Vision AI for quality control in semiconductor fabrication processes"
                },
                {
                    "company": "Dell Technologies",
                    "website": "dell.com",
                    "description": "Multinational computer technology company",
                    "products": "Laptops, servers, storage solutions",
                    "match": "Automation for assembly line optimization and component inspection"
                }
            ],
            "emails": [
                {
                    "company": "Texas Instruments",
                    "subject": "Partnership Opportunity - Vision AI for Semiconductor Manufacturing",
                    "email": "Subject: Partnership Opportunity - Vision AI for Semiconductor Manufacturing\n\nDear Texas Instruments Team,\n\nI hope this email finds you well..."
                }
            ]
        }
    
    async def run_lead_generation(self, task_id: str, prompt: str):
        """Run lead generation in background"""
        try:
            # Initialize task
            self.generation_tasks[task_id] = {
                "task_id": task_id,
                "status": "running",
                "prompt": prompt,
                "created_at": datetime.now(),
                "progress": {
                    "current_step": "Initializing agents",
                    "steps_completed": 0,
                    "total_steps": 5
                }
            }
            
            USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
            
            if USE_MOCK_DATA:
                # Simulate the generation process
                steps = [
                    "Initializing agents",
                    "Researching companies", 
                    "Matching solutions",
                    "Generating leads",
                    "Creating emails"
                ]
                
                for i, step in enumerate(steps):
                    self.generation_tasks[task_id]["progress"] = {
                        "current_step": step,
                        "steps_completed": i + 1,
                        "total_steps": len(steps)
                    }
                    await asyncio.sleep(1)
                
                leads = self.mock_data["leads"]
                emails = self.mock_data["emails"]
            else:
                # Use actual orchestrator
                self.generation_tasks[task_id]["progress"]["current_step"] = "Running AI agents"
                
                orchestrator = LeadGenOrchestrator()
                
                # Run orchestrator in executor to avoid blocking
                results = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: orchestrator.generate_leads(prompt)
                )
                
                leads = results.get("leads", [])
                emails = results.get("emails", [])
            
            # Store results
            self.generation_tasks[task_id]["status"] = "completed"
            self.generation_tasks[task_id]["result"] = {
                "leads": leads,
                "emails": emails
            }
            self.generation_tasks[task_id]["completed_at"] = datetime.now()
            
        except Exception as e:
            self.generation_tasks[task_id]["status"] = "failed"
            self.generation_tasks[task_id]["error"] = str(e)
            self.generation_tasks[task_id]["completed_at"] = datetime.now()
    
    async def get_task_status(self, task_id: str):
        """Get task status and results"""
        if task_id not in self.generation_tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task = self.generation_tasks[task_id]
        
        return {
            "task_id": task_id,
            "status": task["status"],
            "progress": task["progress"],
            "result": task.get("result"),
            "error": task.get("error")
        }
    
    async def get_all_tasks(self):
        """Get all tasks"""
        return {
            "tasks": list(self.generation_tasks.values()),
            "total": len(self.generation_tasks)
        }
    
    async def delete_task(self, task_id: str):
        """Delete a task"""
        if task_id not in self.generation_tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        del self.generation_tasks[task_id]
        return {"message": "Task deleted"}
    
    async def export_results(self, task_id: str, format: str = "json"):
        """Export task results"""
        if task_id not in self.generation_tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task = self.generation_tasks[task_id]
        
        if task["status"] != "completed":
            raise HTTPException(status_code=400, detail="Task not completed")
        
        if format not in ["json", "csv", "xlsx"]:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        result = task["result"]
        
        if format == "json":
            return {
                "leads": result["leads"],
                "emails": result["emails"]
            }
        
        # For CSV/Excel, implement conversion logic here
        return result