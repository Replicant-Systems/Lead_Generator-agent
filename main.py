import typer
from src.config import load_environment
from src.core import LeadGenOrchestrator

app = typer.Typer()

# Load environment variables
load_environment()


@app.command()
def generate(prompt: str):
    """Generate leads and emails based on the given prompt"""
    try:
        orchestrator = LeadGenOrchestrator()
        orchestrator.generate_leads(prompt)
    except Exception as e:
        raise typer.Exit(1)

@app.command()
def serve():
    """Start the web server"""
    import uvicorn
    from api.main import app as api_app
    uvicorn.run(api_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    app()
