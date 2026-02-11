from agent.llm import LLM
from utils.tool_env import ToolEnv
import json

class PlanningAgent:
    def __init__(self, llm: LLM, tool_env: ToolEnv, verbose:bool=True):
        self.llm = llm
        self.tool_env = tool_env
        self.verbose = verbose


    def _get_system_prompt(self) -> str:
        return f"""
        You are a planning agent. You will be given a query, and you need to plan the steps to answer the query. You can call the tools in the tool environment if needed.
        ## Tool Description:
        {self.tool_env.get_tools_desc_list()}

        ## Requirement:
        1. You need to break down the query into several steps, and each step should be a tool calling or a question that can be directly answered by you.
        2. If a step is a tool calling, return the corresponding json string of the tool calling message.
        3. Your response must strictly follow the tool description format.
        4. Your response must strictly follow the tool arguments format.
        5. If a step is a question that can be directly answered by you, return the question as it is.
        """