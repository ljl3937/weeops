from langchain.agents import AgentType
from langchain_community.chat_models.zhipuai import ChatZhipuAI
from ssh_tool import SSHTool
from dotenv import load_dotenv
import os
import json
from langgraph.graph import Graph, StateGraph
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, FunctionMessage, HumanMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.messages import SystemMessage
import re
# 禁用 LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

load_dotenv()

class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    next: str

def create_agent():
    tools = [SSHTool()]
    functions = [convert_to_openai_function(t) for t in tools]
    
    llm = ChatZhipuAI(
        model_name="glm-4-plus",
        temperature=0.3,
        top_p=0.1,
        do_sample=False,
        api_key=os.getenv("ZHIPUAI_API_KEY"),
        verbose=True,
        functions=functions
    )
    
    def should_continue(state: AgentState) -> bool:
        """检查是否应该继续执行"""
        # 检查消息历史长度，避免无限循环
        if len(state["messages"]) > 10:
            return False
            
        last_message = state["messages"][-1]
        if not isinstance(last_message, FunctionMessage):
            return True
        return False

    def call_llm(state: AgentState) -> AgentState:
        """调用 LLM 进行对话"""
        messages = state["messages"]
        # 添加系统提示，引导 LLM 更好地使用工具
        if len(messages) == 1:  # 只有用户输入时
            messages = [
                SystemMessage(content="""你是一个 SSH 远程执行器。你必须严格返回如下格式的纯JSON（不带任何额外字符）：
{"command": "linux命令"}
如果有多个选项，请选择1个直接返回，不要有任何解释
"""),
                *messages
            ]
        response = llm.invoke(messages)

        # 新增清洗逻辑
        try:
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                clean_json = json_match.group().replace('\n', '')
                response.content = clean_json
        except:
            response.content = '{"command": "invalid_format"}'
        return {"messages": [*messages, response], "next": "call_tool"}

    def call_tool(state: AgentState) -> AgentState:
        """执行工具调用"""
        messages = state["messages"]
        last_message = messages[-1]
        
        if not last_message.additional_kwargs.get("function_call"):
            return {"messages": messages, "next": "end"}
            
        action = last_message.additional_kwargs["function_call"]
        action_name = action["name"]
        arguments = json.loads(action["arguments"])
        
        for tool in tools:
            if tool.name == action_name:
                result = tool.run(arguments)
                break
        else:
            result = f"Error: 工具 {action_name} 未找到"
            
        function_message = FunctionMessage(content=str(result), name=action_name)
        return {"messages": [*messages, function_message], "next": "call_llm"}

    def end(state: AgentState) -> AgentState:
        """结束节点"""
        return state

    workflow = StateGraph(AgentState)
    
    workflow.add_node("call_llm", call_llm)
    workflow.add_node("call_tool", call_tool)
    workflow.add_node("end", end)
    
    workflow.set_entry_point("call_llm")
    workflow.add_conditional_edges(
        "call_llm",
        should_continue,
        {
            True: "call_tool",
            False: "end"
        }
    )
    workflow.add_conditional_edges(
        "call_tool",
        should_continue,
        {
            True: "call_llm",
            False: "end"
        }
    )
    
    workflow.set_finish_point("end")
    
    # 设置更高的递归限制
    graph = workflow.compile()
    graph.recursion_limit = 50
    
    return graph

def main():
    # 打印环境变量
    print("\n=== 环境变量 ===")
    print(f"ZHIPUAI_API_KEY: {'*' * 8}{os.getenv('ZHIPUAI_API_KEY')[-4:] if os.getenv('ZHIPUAI_API_KEY') else 'Not Set'}")
    print(f"SSH_HOST: {os.getenv('SSH_HOST') or 'Not Set'}")
    print(f"SSH_USERNAME: {os.getenv('SSH_USERNAME') or 'Not Set'}")
    print(f"SSH_PASSWORD: {'*' * 8 if os.getenv('SSH_PASSWORD') else 'Not Set'}")

    print("\n=== LLM 配置 ===")
    print(f"Model: glm-4")
    print(f"Temperature: 0.5")
    print(f"Top P: 0.7")
    
    print("\n=== Agent 配置 ===")
    print(f"工具列表: ['ssh_tool']")
    print(f"使用 LangGraph 实现")
    
    agent = create_agent()

    while True:
        user_input = input("\n请输入要在服务器上执行的操作（输入 'quit' 退出）: ").strip()
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            break

        try:
            print("\n=== 执行详情 ===")
            print(f"用户输入: {user_input}")
            
            result = agent.invoke({
                "messages": [HumanMessage(content=user_input)]
            })
            # 在 agent.invoke 后检查完整消息流
            print("完整消息历史:")
            for msg in result["messages"]:
                print(f"[{msg.type}] {msg.content}")
            print("\n=== 返回结果 ===")
            messages = result["messages"]
            final_response = messages[-1].content
            print(f"执行结果: {final_response}")
                
        except Exception as e:
            print("\n=== 错误 ===")
            print(f"执行出错: {str(e)}")
            import traceback
            print(f"错误详情:\n{traceback.format_exc()}")

        # 检查连接参数
        print(f"尝试连接: {os.getenv('SSH_HOST')} 用户名: {os.getenv('SSH_USERNAME')}")

if __name__ == "__main__":
    main()