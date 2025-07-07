import json
import pandas as pd
from typing import List, Dict, Any
from rich.console import Console

console = Console()


def save_leads_to_excel(leads: List[Dict[str, Any]], filename: str = "lead_tracker.xlsx") -> bool:
    """Save leads to Excel file"""
    try:
        df = pd.DataFrame(leads)
        df.to_excel(filename, index=False)
        console.print(f"[cyan]Saved leads to [bold]{filename}[/bold][/cyan]")
        return True
    except Exception as e:
        console.print(f"[red]Failed to save Excel file: {e}[/red]")
        return False


def save_emails_to_json(emails: List[Dict[str, Any]], filename: str = "emails.json") -> bool:
    """Save emails to JSON file"""
    try:
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(emails, f, indent=2, ensure_ascii=False)
        console.print(f"[cyan]Saved emails to [bold]{filename}[/bold][/cyan]")
        return True
    except Exception as e:
        console.print(f"[red]Failed to save emails file: {e}[/red]")
        return False