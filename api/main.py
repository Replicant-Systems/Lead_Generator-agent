"""FastAPI backend for LeadGen AI web interface"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import load_environment
from .routes import leads, tasks

# Load environment variables
load_environment()

app = FastAPI(
    title="LeadGen AI API",
    description="AI-powered lead generation with multi-agent orchestration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router)
app.include_router(tasks.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "LeadGen AI API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)