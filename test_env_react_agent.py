from agent.env_agent import EnvAgent
from utils.tool_collection.data_analysis_tool import analyze_data_tool
from utils.tool_collection.file_tool import load_file_tool, write_file_tool
from utils.tool_env import ToolEnv
from utils.var_env import VarEnv
from agent.llm import LLM



tool_env = ToolEnv()
var_env = VarEnv()
tool_env.register_tool([analyze_data_tool, load_file_tool, write_file_tool])

agent = EnvAgent(LLM(), tool_env, var_env)

# python test_data_analysis_agent.py
if __name__ == "__main__":
    print(agent.call('Analyze the file at "documents/ChocolateSales.csv", and write a report to the file at "documents/output/ChocolateSales_report.txt".'))