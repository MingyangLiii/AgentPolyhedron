from agent.tool_calling_agent import ToolCallingAgent
from utils.tool_collection.time_tool import tool_get_current_time_by_timezone
from utils.tool_collection.calc_tool import tool_multiply, tool_divide, tool_power
from utils.tool_env import ToolEnv
from agent.llm import LLM



tool_env = ToolEnv()
# tool_env.register_tool(tool_get_current_time_by_timezone)
# tool_env.register_tool(tool_multiply)

agent = ToolCallingAgent(LLM(), tool_env)


if __name__ == "__main__":
    # print(agent.tool_env.get_tools_desc_list_short())
    # print(agent.tool_env.get_tools_desc_list())

    # print(agent.call("What is the current time in Atlanta?"))
    # print(agent.call('what is the result of 1045.933 / 8344.92?'))

    agent.tool_env.register_tool(tool_get_current_time_by_timezone)
    # agent.tool_env.register_tool(tool_multiply)
    agent.tool_env.register_tool(tool_divide)
    # agent.tool_env.register_tool(tool_power)


    print(agent.call("What is the current time in Atlanta?"))
    print(agent.call('what is the result of 1045.933 / 8344.92?'))
    

