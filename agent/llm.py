from dotenv import load_dotenv
import os
from openai import OpenAI

env = load_dotenv()
# print(os.getenv("DEEPSEEK_API_KEY")) 


class LLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com"
        )
            
    def call(self, messages):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content




