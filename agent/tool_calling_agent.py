from typing import List, Dict
from agent.llm import LLM
from utils.tool_env import ToolEnv
import json

class ToolCallingAgent:
    def __init__(self, llm: LLM, tool_env: ToolEnv, verbose:bool=True):
        self.llm = llm
        self.tool_env = tool_env
        self.verbose = verbose


    
    def _get_system_prompt(self, query) -> List[Dict]:
        return [{"role": "system", "content": f"""
        You are a tool calling agent. You will be given a list of tool name and arguments, and you can call the tool with the arguments if needed.
        ## Tool Description:
        {self.tool_env.get_tools_desc_list()}

        ## Requirement:
        1. If your want to call a tool, return the corresponding json string of the tool calling message.
        1. Your response must strictly follow the tool description format.
        2. Your response must strictly follow the tool arguments format.
        3. If you do not need a tool, only return 'None'.
        """},
            {"role": "user", "content": query}
        ]
    
    

    def _get_response_prompt(self, tool_calling_res: str, query: str) -> List[Dict]:
        return [
                {"role": "system", "content": "You are an intelligent assistant. Please answer the query based on the search result you get."},
                {"role": "assistant", "content": "Search Result: " + tool_calling_res},
                {"role": "user", "content": query}
            ]
    
    def _get_default_prompt(self, query: str) -> List[Dict]:
        return [
            {"role": "system", "content": "You are an intelligent assistant. Please answer the user's question"},
            {"role": "user", "content": query}
        ]

    def call(self, query: str) -> str:
        # No available tool, directly call LLM to answer
        if self.tool_env.tools == []:
            return self.llm.call(self._get_default_prompt(query))


        system_prompt = self._get_system_prompt(query)
        tool_calling_msg = self.llm.call(system_prompt)

        if self.verbose:
            print("Invoking Tool...")
            print(tool_calling_msg)


        # Without tool calling
        if "None" in tool_calling_msg and len(tool_calling_msg) <= 5:
            return self.llm.call(self._get_default_prompt(query))
        

        # With tool calling
        try:
            tool_calling_res = self.tool_env.call(tool_calling_msg) 

            if self.verbose:
                print("Tool Calling Result:")
                print(tool_calling_res)

            response_prompt = self._get_response_prompt(tool_calling_res, query)
            return self.llm.call(response_prompt) 


        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse tool calling message: {e}")

