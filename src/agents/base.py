import autogen
from typing import Dict, Any


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config
    
    def create_user_proxy(self) -> autogen.UserProxyAgent:
        """Create user proxy agent"""
        return autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            code_execution_config=False,
            system_message="You are the founder of Replicant Systems, a company that builds industrial automation solutions with AI and vision systems."
        )
