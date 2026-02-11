from typing import Callable, Dict, Union, List
import json
from utils.tool import Tool



class ToolEnv:
    def __init__(self):
        self.tools = []


    def call(self, message: Union[Dict, str]) -> str:
        """
        Example Message:
        {
        "method": "tools/call",
        "params": {
            "name": "get_weather",
            "arguments": {
            "location": "type: string \n description: City name or zip code \n required: True"
                }
            }
        }
        """
        
        if isinstance(message, str):
            message = json.loads(message)

        func = self.get_tool_func(message["params"]["name"]) # type: ignore
        arguments = message["params"]["arguments"] # type: ignore

        arguments_list = []
        for key, value in arguments.items(): # type: ignore
            arguments_list.append(value)
            
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


    def delete_tool(self, name:str) -> None:
        for tool in self.tools:
            if tool.name == name:
                self.tools.remove(tool)
                return
        raise ValueError(f"Tool {name} not found")
    
    



