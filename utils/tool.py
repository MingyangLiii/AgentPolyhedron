from typing import Callable, Dict, List, Union
import json


"""
Example
"tools": [
    {
        "name": "get_weather",
        "title": "Weather Information Provider",
        "description": "Get current weather information for a location",
        "inputSchema": {
            "type": "object",
            "properties": {
            "location": {
                "type": "string",
                "description": "City name or zip code"
                }
            },
            "required": ["location"]
        }
    }
]
"""



class Property:
    def __init__(self,
                 name:str,
                 type:str,
                 description:str):
        self.name = name
        self.type = type
        self.description = description

    def get_property(self):
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description
        }


class InputSchema:
    def __init__(self,
                 properties:Union[List[Property], List[Dict]],
                 required:List[str]):
                 
        self.properties = properties
        self.required = required

    def get_input_schema(self):
        properties_return = {}

        for p in self.properties:
            if isinstance(p, Property):
                properties_return[p.name] = {"type": p.type, "description": p.description}
            elif isinstance(p, Dict):
                properties_return[p["name"]] = {"type": p["type"], "description": p["description"]}
            else:
                raise ValueError("properties must be a list of Property or Dict")
            
        return {
            "type": "object",
            "properties": properties_return,
            "required": self.required
        }
        

class Tool:
    def __init__(self,
                 name:str,
                 title:Union[str, None],
                 description:str,
                 func:Callable,
                 inputSchema:Union[InputSchema, Dict]):
        

        self.name = name

        if title is None:
            self.title = name
        else:
            self.title = title

        self.description = description
        self.func = func

        if isinstance(inputSchema, InputSchema):
            self.inputSchema = inputSchema.get_input_schema()
        elif isinstance(inputSchema, Dict):
            self.inputSchema = inputSchema
        else:
            raise ValueError("inputSchema must be a InputSchema or Dict")
      
        
    def get_tool_info(self):
        arguments = {}
        for key, value in self.inputSchema["properties"].items():
            # 使用列表拼接提高性能
            desc_parts = [f"{k}: {v}" for k, v in value.items()]
            desc_parts.append(f"required: {key in self.inputSchema['required']}")
            arguments[key] = " \n ".join(desc_parts)

        tool = {
            "method": "tools/call",
            "params": {
                "name": self.name,
                "arguments": arguments
            }
        }
        return json.dumps(tool, indent=2, ensure_ascii=False)
    

    def get_func(self):
        return self.func
    
    




if __name__ == "__main__":
    example = {
        "name": "get_weather",
        "title": "Weather Information Provider",
        "description": "Get current weather information for a location",
        "inputSchema": {
            "type": "object",
            "properties": {
            "location": {
                "type": "string",
                "description": "City name or zip code"
                }
            },
            "required": ["location"]
        }
    }
    def get_weather(location: str):
        return f"The weather in {location} is sunny."



    tool = Tool(
        name=example['name'],
        title=example['title'],
        description=example['description'],
        func=get_weather, # type: ignore
        inputSchema=example['inputSchema']
    )

    print(tool.get_tool_info())
