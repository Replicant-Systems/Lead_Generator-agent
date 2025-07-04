import autogen
from .base import BaseAgent


class MatcherAgent(BaseAgent):
    """Agent responsible for matching companies with solutions"""
    
    def create_agent(self) -> autogen.AssistantAgent:
        """Create matcher agent"""
        return autogen.AssistantAgent(
            name="Matcher",
            llm_config=self.llm_config,
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