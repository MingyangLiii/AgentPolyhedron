from agent.react_agent import ReactAgent
from utils.tools.time_tool import tool_get_current_time_by_timezone
from utils.tools.calc_tool import tool_multiply, tool_divide, tool_power
from utils.tool_env import ToolEnv
from agent.llm import LLM



tool_env = ToolEnv()
# tool_env.register_tool(tool_get_current_time_by_timezone)
math_tools = [tool_multiply, tool_divide, tool_power]
tool_env.register_tool(math_tools)


agent = ReactAgent(LLM(), tool_env)


if __name__ == "__main__":
    # print(agent.tool_env.get_tools_desc_list_short())
    # print(agent.tool_env.get_tools_desc_list())

    print(agent.call('what is the result of (1045.933 / 8344.92 * 1345.7) ^ 2? You should use the tool to calculate instead of calculating by yourself.'))