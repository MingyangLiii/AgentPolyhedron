from typing import Dict, List
from agent.llm import LLM
from utils.tool_env import ToolEnv
import json

class ReactAgent:
    def __init__(self, llm: LLM, tool_env: ToolEnv, verbose:bool=True):
        self.llm = llm
        self.tool_env = tool_env
        self.verbose = verbose

    def _get_thought_prompt(self, task: str, history: List[str]) -> List[Dict]:
        history = "\n".join(history) # type: ignore
        return [
            {"role": "system", "content": "You are a methodical problem solver. Think step-by-step."},
            {"role": "user", "content": f"""## Task: {task}

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
            "role": "system", "content": f"""You are a tool calling agent. You will be given a list of tool name and arguments, and you can call the tool with the arguments if needed.
            ## Tool Description:
            {self.tool_env.get_tools_desc_list()}

            ## Requirement:
            1. If your want to call a tool, take the action 'ToolCall'.
            2. If the task is solved, take the action 'Finish'.

            ## Output Format:
            {{
                "action": "ToolCall" or "Finish",
                "content": "If action is 'ToolCall', content should be the json string of the tool calling message. If action is 'Finish', content should be 'Finish'."
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

            if "Finish" in msg["action"]: # type: ignore
                response_prompt = self._get_response_prompt(task, history)
                return self.llm.call(response_prompt) # type: ignore

            elif "ToolCall" in msg["action"]: # type: ignore
                try:
                    tool_calling_msg = msg["content"] # type: ignore
                    tool_calling_res = self.tool_env.call(tool_calling_msg) # type: ignore

                    history.append(f"Thought {i+1}: {thought}")
                    history.append(f"Action {i+1}: {action}")
                    history.append(f"Tool Result {i+1}: {tool_calling_res}")
                except Exception as e:
                    raise ValueError(f"Tool calling failed with error: {e}")

            else:
                raise ValueError(f"Invalid action in message: {msg}")
            
            

        response_prompt = self._get_response_prompt(task, history)
        return self.llm.call(response_prompt) # type: ignore


    


