from typing import Callable, Dict, Union, List
import json
from utils.tool import Tool
from utils.var_env import VarEnv



class ToolEnv:
    def __init__(self):
        self.tools = []
        self.variables = {}


    def call(self, message: Union[Dict, str], var_env: Union[VarEnv, None]=None) -> str:
        """
        Example Message:
        {
            "method": "tools/call",
            "params": {
                "name": "get_weather",
                "arguments": {"location": "Beijing"}
            }
        }
        """
        
        if isinstance(message, str):
            message = json.loads(message)

        if "params" in message:
            tool_name = message["params"]["name"] # type: ignore
            arguments = message["params"]["arguments"] # type: ignore
        else:
            tool_name = message["name"] # type: ignore
            arguments = message["arguments"] # type: ignore

        func = self.get_tool_func(tool_name)

        arguments_list = []
        

        for key, value in arguments.items(): # type: ignore
            arguments_list.append(value)
        
        if var_env is not None:
            for i in range(len(arguments_list)):
                if var_env.contains_var(arguments_list[i]):
                    arguments_list[i] = var_env.get_var(arguments_list[i])

            
        return func(*arguments_list)



    
    def get_tools_desc_list(self) -> str:
        tools_list = []
        for tool in self.tools:
            tools_list.append(tool.get_tool_info())
        return "\n".join(tools_list)
    
    def get_tools_desc_list_short(self) -> str:
        tools_list = []
        for tool in self.tools:
            tools_list.append(tool.name)
        return "\n".join(tools_list)

    def get_tool(self, name:str) -> Tool:
        for tool in self.tools:
            if tool.name == name:
                return tool
        
        raise ValueError(f"Tool {name} not found")
    
    def get_tool_func(self, name:str) -> Callable:
        for tool in self.tools:
            if tool.name == name:
                return tool.func
        
        raise ValueError(f"Tool {name} not found")
        
    def get_tool_info(self, name:str) -> str:
        for tool in self.tools:
            if tool.name == name:
                return tool.get_tool_info()
        
        raise ValueError(f"Tool {name} not found")
    
    def get_tool_count(self) -> int:
        return len(self.tools)
    

    def register_tool(self, tool:Union[Tool, List[Tool]]) -> None:
        if isinstance(tool, Tool):
            self.tools.append(tool)
        elif isinstance(tool, List):
            self.tools.extend(tool)
        else:
            raise ValueError("Tool should be of type Tool or List[Tool]")


    def delete_tool(self, name:str) -> None:
        for tool in self.tools:
            if tool.name == name:
                self.tools.remove(tool)
                return
        raise ValueError(f"Tool {name} not found")
    
    



