from typing import Dict, List
from agent.llm import LLM
from utils.tool_env import ToolEnv
from utils.var_env import VarEnv
import json

class EnvAgent:
    def __init__(self, llm: LLM, tool_env: ToolEnv, var_env: VarEnv, verbose:bool=True):
        self.llm = llm
        self.tool_env = tool_env
        self.var_env = var_env
        self.verbose = verbose

    def _get_thought_prompt(self, task: str, history: List[str]) -> List[Dict]:
        history = "\n".join(history) # type: ignore
        return [
            {"role": "system", "content": "You are a methodical problem solver. Think step-by-step."},
            {"role": "user", "content": f"""## Task: {task}
             
            ## Available Variables:
            {self.var_env.list_vars()}

            ## Available Tools:
            {self.tool_env.get_tools_desc_list_short()}
            
            ## Previous steps: {history}

            ## Instructions:
            Think carefully about what to do next. Consider:
            1. What information do I need?
            2. Which tool is most appropriate?
            3. How will this help solve the task?

            ## Output:
            Your thought:"""
        }]
    
    def _get_action_prompt(self, thought: str) -> List[Dict]:
        return [{
            "role": "system", "content": f"""You are a tool calling agent. You will be given a list of tool name and arguments, and you can call the following tool with the arguments if needed.
            However, your tool calling should not be out of the available tools as described below. 

            ## Available Variables:
            {self.var_env.list_vars()}
            
            ## Tool Description:
            {self.tool_env.get_tools_desc_list()}

            ## Requirement:
            1. If your want to call a tool, call the method 'tools/call'.
            2. If the task is solved, call the method "finish".
            3. You should not repetitively call tools. If you have called a tool and get the result, you should think about the result and decide what to do next, instead of calling the same tool again.
            4. You can use the available variables as arguments when calling tools. The variables are set by the tool calling results in previous steps. You can also use the tool calling results in previous steps as arguments when calling tools.

            ## Output Format:
            Example 1 (calling tool):
            {{
                "method": "tools/call",
                "params": {{
                    "name": "get_weather",
                    "arguments": {{"location": "Beijing"}}
                }}
            }}

            Example 2 (finishing task):
            {{
                "method": "finish",
                "params": {{
                    "result": "The task has been completed successfully"
                }}
            }} 
            """},
            {"role": "user", "content": f"""## Thought: {thought}"""
        }]
    
    def _get_response_prompt(self, task: str, history: list) -> List[Dict]:
        history = "\n".join(history) # type: ignore
        return [{
            "role": "system", "content": f"""You are a helpful assistant. You will be given a task and the history of the previous steps. 
            Your goal is to provide a final response to user."""},
            {"role": "user", "content": f"""## Task: {task}
            ## Previous steps: {history}"""
        }]
    

    def call(self, task: str, max_iter: int = 5) -> str:
        history = []
        for i in range(max_iter):
            thought_prompt = self._get_thought_prompt(task, history) # type: ignore
            thought = self.llm.call(thought_prompt)

            action_prompt = self._get_action_prompt(thought) # type: ignore
            action = self.llm.call(action_prompt)


            if self.verbose:
                print(f"Thought {i+1}: {thought}")
                print("-----------------------------")
                print(f"Action {i+1}: {action}")
                print("-----------------------------")

            
            msg = json.loads(action) # type: ignore

            if "finish" in msg["method"]: # type: ignore
                response_prompt = self._get_response_prompt(task, history)
                return self.llm.call(response_prompt) # type: ignore

            elif "tools/call" in msg["method"]: # type: ignore
                try: 
                    tool_calling_res = self.tool_env.call(msg, self.var_env) # type: ignore

                    if type(tool_calling_res) == str:
                        history.append(f"Thought {i+1}: {thought}")
                        history.append(f"Action {i+1}: {action}")
                        history.append(f"Tool Result {i+1}: {tool_calling_res}")
                    else:
                        self.var_env.set_var(f"var_{i+1}", tool_calling_res)
                        history.append(f"Thought {i+1}: {thought}")
                        history.append(f"Action {i+1}: {action}")
                        history.append(f"Tool Result {i+1}: variable 'var_{i+1}' is set.")


                except Exception as e:
                    raise ValueError(f"Tool calling failed with error: {e}")

            else:
                raise ValueError(f"Invalid action in message: {msg}")
            
            

        response_prompt = self._get_response_prompt(task, history)
        return self.llm.call(response_prompt) # type: ignore