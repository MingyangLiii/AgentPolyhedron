from agent.react_agent import ReactAgent
from utils.tools.data_analysis_tool import analyze_data_tool
from utils.tool_env import ToolEnv
from agent.llm import LLM



tool_env = ToolEnv()
tool_env.register_tool(analyze_data_tool)

agent = ReactAgent(LLM(), tool_env)

# python test_data_analysis_agent.py
if __name__ == "__main__":
    print(agent.call('Analyze the "documents/ChocolateSales.csv"'))
