import autogen
from .base import BaseAgent


class ResearcherAgent(BaseAgent):
    """Agent responsible for researching companies"""
    
    def create_agent(self) -> autogen.AssistantAgent:
        """Create researcher agent"""
        return autogen.AssistantAgent(
            name="Researcher",
            llm_config=self.llm_config,
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