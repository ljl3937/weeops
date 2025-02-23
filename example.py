from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models.zhipuai import ChatZhipuAI
from ssh_tool import SSHTool
from dotenv import load_dotenv
import os
import json

load_dotenv()

def main():
    # 打印环境变量
    print("\n=== 环境变量 ===")
    print(f"ZHIPUAI_API_KEY: {'*' * 8}{os.getenv('ZHIPUAI_API_KEY')[-4:] if os.getenv('ZHIPUAI_API_KEY') else 'Not Set'}")
    print(f"SSH_HOST: {os.getenv('SSH_HOST') or 'Not Set'}")
    print(f"SSH_USERNAME: {os.getenv('SSH_USERNAME') or 'Not Set'}")
    print(f"SSH_PASSWORD: {'*' * 8 if os.getenv('SSH_PASSWORD') else 'Not Set'}")

    print("\n=== LLM 配置 ===")
    llm = ChatZhipuAI(
        model_name="glm-4",
        temperature=0.5,
        top_p=0.7,
        api_key=os.getenv("ZHIPUAI_API_KEY"),
        verbose=True
    )
    print(f"Model: glm-4")
    print(f"Temperature: 0.5")
    print(f"Top P: 0.7")
    
    print("\n=== Agent 配置 ===")
    tools = [SSHTool()]
    print(f"工具列表: {[tool.name for tool in tools]}")
    print(f"Agent 类型: {AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION}")
    
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True
    )

    while True:
        user_input = input("\n请输入要在服务器上执行的操作（输入 'quit' 退出）: ")
        if user_input.lower() == 'quit':
            break

        try:
            print("\n=== 执行详情 ===")
            print(f"用户输入: {user_input}")
            
            result = agent.invoke({
                "input": user_input
            })
            
            print("\n=== 返回结果 ===")
            print(f"原始结果类型: {type(result)}")
            print(f"原始结果内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 检查是否包含工具调用结果
            if isinstance(result, dict) and 'output' in result:
                output = result['output']
                print("\n=== 解析结果 ===")
                print(f"输出内容: {output}")
                
                # 如果输出是字符串形式的Python代码块，提取实际的命令并执行
                if "```python" in output and "tool_call" in output:
                    # 提取命令参数
                    start = output.find("command='") + 9
                    end = output.find("'", start)
                    if start > 8 and end > start:
                        command = output[start:end]
                        print(f"\n=== SSH 命令执行 ===")
                        print(f"解析出的命令: {command}")
                        # 直接执行命令
                        ssh_tool = SSHTool()
                        actual_result = ssh_tool.run({
                            "command": command,
                            "host": os.getenv("SSH_HOST"),
                            "username": os.getenv("SSH_USERNAME"),
                            "password": os.getenv("SSH_PASSWORD")
                        })
                        print(f"\n命令执行结果:\n{actual_result}")
                    else:
                        print("\n=== 错误 ===")
                        print("无法解析命令")
                else:
                    print(f"\n最终输出:\n{output}")
            else:
                print(f"\n最终输出:\n{result}")
                
        except Exception as e:
            print("\n=== 错误 ===")
            print(f"执行出错: {str(e)}")
            import traceback
            print(f"错误详情:\n{traceback.format_exc()}")

if __name__ == "__main__":
    main()