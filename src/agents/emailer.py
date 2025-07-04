import autogen
from .base import BaseAgent


class EmailerAgent(BaseAgent):
    """Agent responsible for generating emails"""
    
    def create_agent(self) -> autogen.AssistantAgent:
        """Create emailer agent"""
        return autogen.AssistantAgent(
            name="EmailAgent",
            llm_config=self.llm_config,
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
