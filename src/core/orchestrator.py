import autogen
from typing import Tuple, Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel

from ..config import get_llm_config
from ..agents import ResearcherAgent, MatcherAgent, LeadLoggerAgent, EmailerAgent, BaseAgent
from ..utils import (
    extract_json_from_text, 
    validate_leads_structure, 
    validate_emails_structure,
    save_leads_to_excel,
    save_emails_to_json
)


class LeadGenOrchestrator:
    """Main orchestrator for the lead generation process"""
    
    def __init__(self):
        self.console = Console()
        self.llm_config = None
        self.agents = {}
    
    def _setup_agents(self):
        """Setup all agents"""
        try:
            self.llm_config = get_llm_config()
        except ValueError as e:
            self.console.print(f"[red]Configuration Error: {e}[/red]")
            raise
        
        # Create agent instances
        base_agent = BaseAgent(self.llm_config)
        researcher = ResearcherAgent(self.llm_config)
        matcher = MatcherAgent(self.llm_config)
        logger = LeadLoggerAgent(self.llm_config)
        emailer = EmailerAgent(self.llm_config)
        
        # Create actual agents
        self.agents = {
            'user': base_agent.create_user_proxy(),
            'researcher': researcher.create_agent(),
            'matcher': matcher.create_agent(),
            'logger': logger.create_agent(),
            'emailer': emailer.create_agent()
        }
    
    def _process_messages(self, messages: List[Dict[str, Any]]) -> Tuple[Optional[List], Optional[List]]:
        """Process messages to extract leads and emails"""
        leads, emails = None, None
        
        self.console.print("\n[blue]Processing agent outputs...[/blue]")
        
        for msg in reversed(messages):
            if msg.get("name") == "LeadLogger" and leads is None:
                try:
                    content = msg["content"].strip()
                    self.console.print(f"[dim]LeadLogger content preview: {content[:100]}...[/dim]")
                    leads = extract_json_from_text(content)
                    
                    if leads and validate_leads_structure(leads):
                        self.console.print(f"[green]✔ Got {len(leads)} structured leads from LeadLogger[/green]")
                    else:
                        self.console.print(f"[yellow]⚠ Invalid lead structure from LeadLogger[/yellow]")
                        leads = None
                except Exception as e:
                    self.console.print(f"[red]Lead parsing failed: {e}[/red]")
            
            if msg.get("name") == "EmailAgent" and emails is None:
                try:
                    content = msg["content"].strip()
                    self.console.print(f"[dim]EmailAgent content preview: {content[:100]}...[/dim]")
                    emails = extract_json_from_text(content)
                    
                    if emails and validate_emails_structure(emails):
                        self.console.print(f"[green]✔ Got {len(emails)} emails from EmailAgent[/green]")
                    else:
                        self.console.print(f"[yellow]⚠ Invalid email structure from EmailAgent[/yellow]")
                        self.console.print(f"[dim]Raw content: {content[:200]}...[/dim]")
                        emails = None
                except Exception as e:
                    self.console.print(f"[red]Email parsing failed: {e}[/red]")
        
        return leads, emails
    
    def _save_results(self, leads: Optional[List], emails: Optional[List]):
        """Save results to files"""
        if leads:
            save_leads_to_excel(leads)
        
        if emails:
            save_emails_to_json(emails)
    
    def generate_leads(self, prompt: str):
        """Main method to generate leads and emails"""
        self.console.print(Panel(f"[bold]LeadGen Prompt:[/bold] {prompt}", title="📌 Prompt"))
        
        try:
            # Setup agents
            self._setup_agents()
            
            # Create group chat
            agent_list = list(self.agents.values())
            groupchat = autogen.GroupChat(
                agents=agent_list,
                messages=[],
                max_round=15,
                speaker_selection_method="round_robin"
            )
            
            manager = autogen.GroupChatManager(
                groupchat=groupchat,
                llm_config=self.llm_config
            )
            
            # Initiate the chat
            self.agents['user'].initiate_chat(manager, message=prompt)
            
            # Process results
            leads, emails = self._process_messages(groupchat.messages)
            
            # Save results
            self._save_results(leads, emails)
            
            # Summary
            if not leads and not emails:
                self.console.print("[yellow]⚠ No valid data was generated. Check the conversation flow.[/yellow]")
            else:
                self.console.print(f"[green]✔ Process completed successfully![/green]")
                
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {e}[/red]")
            raise