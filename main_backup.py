import os
import json
import typer
import pandas as pd
from dotenv import load_dotenv
import autogen
from rich.console import Console
from rich.panel import Panel
import re

app = typer.Typer()
console = Console()

# ─── Load Environment ─────────────────────────────────────────────────────
load_dotenv()

# ─── LLM Config ───────────────────────────────────────────────────────────
def get_llm_config():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env file")
    return {
        "config_list": [{
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "api_key": api_key,
            "base_url": "https://api.groq.com/openai/v1",
        }],
        "temperature": 0.4
    }

# ─── Helper Functions ─────────────────────────────────────────────────────
def extract_json_from_text(text):
    """Extract JSON from text that might contain other content"""
    # Remove common markdown code block markers
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    
    # Look for JSON array pattern (more permissive)
    json_patterns = [
        r'\[[\s\S]*?\]',  # Array pattern (most permissive)
        r'\{[\s\S]*?\}',  # Object pattern
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                parsed = json.loads(match.strip())
                # Ensure it's a list for our use case
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict):
                    return [parsed]  # Convert single object to list
            except json.JSONDecodeError:
                continue
    
    # Try parsing the whole text after cleaning
    try:
        # Remove any leading/trailing non-JSON text
        cleaned_text = text.strip()
        # Find the first [ and last ]
        start_idx = cleaned_text.find('[')
        end_idx = cleaned_text.rfind(']')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_text = cleaned_text[start_idx:end_idx+1]
            return json.loads(json_text)
    except (json.JSONDecodeError, ValueError):
        pass
    
    return None

def validate_leads_structure(leads):
    """Validate that leads have required fields"""
    if not isinstance(leads, list):
        return False
    
    required_fields = ['company', 'description']
    for lead in leads:
        if not isinstance(lead, dict):
            return False
        if not all(field in lead for field in required_fields):
            return False
    return True

def validate_emails_structure(emails):
    """Validate that emails have required fields"""
    if not isinstance(emails, list):
        return False
    
    required_fields = ['company', 'email']
    for email in emails:
        if not isinstance(email, dict):
            return False
        if not all(field in email for field in required_fields):
            return False
    return True

# ─── Agent Setup ──────────────────────────────────────────────────────────
def create_agents():
    """Create and return all agents with proper error handling"""
    try:
        llm_config = get_llm_config()
    except ValueError as e:
        console.print(f"[red]❌ Configuration Error: {e}[/red]")
        raise typer.Exit(1)

    user = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        code_execution_config=False,
        system_message="You are the founder of Replicant Systems, a company that builds industrial automation solutions with AI and vision systems."
    )

    researcher = autogen.AssistantAgent(
        name="Researcher",
        llm_config=llm_config,
        system_message="""
You are a business researcher. Given the user's prompt (industry, location, need), find 3-5 relevant companies.

IMPORTANT: Return ONLY a valid JSON array with this exact structure:
[
  {
    "company": "Company Name",
    "website": "https://example.com or N/A if not available",
    "description": "Brief company description",
    "products": "Main products/services offered"
  }
]

Do not include any text before or after the JSON array.
"""
    )

    matcher = autogen.AssistantAgent(
        name="Matcher",
        llm_config=llm_config,
        system_message="""
You analyze company information and suggest how Replicant Systems (vision AI + industrial automation) can help them.

IMPORTANT: Return ONLY a valid JSON array with this exact structure:
[
  {
    "company": "Company Name",
    "match": "Specific suggestion for how Replicant Systems can help this company"
  }
]

Do not include any text before or after the JSON array.
"""
    )

    logger = autogen.AssistantAgent(
        name="LeadLogger",
        llm_config=llm_config,
        system_message="""
You combine company information with match suggestions into a final lead list.

IMPORTANT: Return ONLY a valid JSON array with this exact structure:
[
  {
    "company": "Company Name",
    "website": "Website URL or N/A",
    "description": "Company description",
    "products": "Products/services",
    "match": "How Replicant Systems can help"
  }
]

Do not include any text before or after the JSON array.
"""
    )

    emailer = autogen.AssistantAgent(
        name="EmailAgent",
        llm_config=llm_config,
        system_message="""
You write personalized emails for each lead using the company information and Replicant's capabilities.

CRITICAL: You MUST return ONLY a valid JSON array. No explanatory text, no markdown, no code blocks.

Example format:
[
  {
    "company": "ABC Manufacturing",
    "email": "Subject: Partnership Opportunity - Industrial Automation Solutions\\n\\nDear ABC Manufacturing Team,\\n\\nI hope this email finds you well. I'm reaching out from Replicant Systems, a company specializing in AI-powered vision systems and industrial automation solutions.\\n\\nBest regards,\\nReplicant Systems Team"
  }
]

Remember: Return ONLY the JSON array, nothing else.
"""
    )

    return user, researcher, matcher, logger, emailer, llm_config

# ─── Main Function ────────────────────────────────────────────────────────
@app.command()
def generate(prompt: str):
    """Generate leads and emails based on the given prompt"""
    console.print(Panel(f"[bold]LeadGen Prompt:[/bold] {prompt}", title="📌 Prompt"))
    
    try:
        user, researcher, matcher, logger, emailer, llm_config = create_agents()
        
        groupchat = autogen.GroupChat(
            agents=[user, researcher, matcher, logger, emailer],
            messages=[],
            max_round=15,  # Increased from 10 to give more time
            speaker_selection_method="round_robin"
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=llm_config
        )

        # Initiate the chat
        user.initiate_chat(manager, message=prompt)

        leads, emails = None, None

        # Process messages in reverse order to get the latest results
        console.print("\n[blue]📋 Processing agent outputs...[/blue]")
        
        for msg in reversed(groupchat.messages):
            if msg.get("name") == "LeadLogger" and leads is None:
                try:
                    content = msg["content"].strip()
                    console.print(f"[dim]LeadLogger content preview: {content[:100]}...[/dim]")
                    leads = extract_json_from_text(content)
                    
                    if leads and validate_leads_structure(leads):
                        console.print(f"[green]✔ Got {len(leads)} structured leads from LeadLogger[/green]")
                    else:
                        console.print(f"[yellow]⚠ Invalid lead structure from LeadLogger[/yellow]")
                        leads = None
                except Exception as e:
                    console.print(f"[red]❌ Lead parsing failed: {e}[/red]")
            
            if msg.get("name") == "EmailAgent" and emails is None:
                try:
                    content = msg["content"].strip()
                    console.print(f"[dim]EmailAgent content preview: {content[:100]}...[/dim]")
                    emails = extract_json_from_text(content)
                    
                    if emails and validate_emails_structure(emails):
                        console.print(f"[green]✔ Got {len(emails)} emails from EmailAgent[/green]")
                    else:
                        console.print(f"[yellow]⚠ Invalid email structure from EmailAgent[/yellow]")
                        console.print(f"[dim]Raw content: {content[:200]}...[/dim]")
                        emails = None
                except Exception as e:
                    console.print(f"[red]❌ Email parsing failed: {e}[/red]")

        # Save results
        if leads:
            try:
                df = pd.DataFrame(leads)
                df.to_excel("lead_tracker.xlsx", index=False)
                console.print("[cyan]📁 Saved leads to [bold]lead_tracker.xlsx[/bold][/cyan]")
            except Exception as e:
                console.print(f"[red]❌ Failed to save Excel file: {e}[/red]")

        if emails:
            try:
                with open("emails.json", "w", encoding='utf-8') as f:
                    json.dump(emails, f, indent=2, ensure_ascii=False)
                console.print("[cyan]📁 Saved emails to [bold]emails.json[/bold][/cyan]")
            except Exception as e:
                console.print(f"[red]❌ Failed to save emails file: {e}[/red]")

        # Summary
        if not leads and not emails:
            console.print("[yellow]⚠ No valid data was generated. Check the conversation flow.[/yellow]")
        else:
            console.print(f"[green]✔ Process completed successfully![/green]")

    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        raise typer.Exit(1)

# ─── CLI Entry ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app()