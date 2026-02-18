from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import List, Dict

env = load_dotenv()

class LLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get('API_KEY'),
            base_url=os.environ.get('BASE_URL')
        )
            
    def call(self, messages: List[Dict]) -> str:
        response = self.client.chat.completions.create(
            model=os.environ.get('MODEL'), # type: ignore
            messages=messages, # type: ignore
            stream=False
        ) # type: ignore
        return response.choices[0].message.content




