from typing import Any, Dict, Optional, Union, List
import json



class VarEnv:
    def __init__(self):
        self.variables = {}

    def set_var(self, name: str, value: Any):
        self.variables[name] = value

    def get_var(self, name: str) -> Optional[Any]:
        return self.variables.get(name)
    
    def delete_var(self, name: str):
        if name in self.variables:
            del self.variables[name]

    def contains_var(self, name: str) -> bool:
        return name in self.variables.keys()
    
    def list_vars(self) -> str:
        return str([key for key in self.variables.keys()])
    
    def __getitem__(self, key: str) -> Any:
        return self.variables[key]
    
