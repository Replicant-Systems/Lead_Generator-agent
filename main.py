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


if __name__ == "__main__":
    app()
