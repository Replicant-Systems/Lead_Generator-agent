import autogen
from .base import BaseAgent


class LeadLoggerAgent(BaseAgent):
    """Agent responsible for logging leads"""
    
    def create_agent(self) -> autogen.AssistantAgent:
        """Create lead logger agent"""
        return autogen.AssistantAgent(
            name="LeadLogger",
            llm_config=self.llm_config,
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