from ssh_tool import SSHTool
from dotenv import load_dotenv
import os

def test_ssh_commands():
    # 加载环境变量
    load_dotenv()
    
    # 创建 SSH 工具实例
    ssh_tool = SSHTool()
    
    # 要测试的命令列表
    commands = [
        "pwd",  # 查看当前目录
        "ls -la",  # 列出文件
        "df -h",  # 查看磁盘使用情况
        "uname -a",  # 查看系统信息
    ]
    
    # 执行每个命令并打印结果
    for cmd in commands:
        print(f"\n执行命令: {cmd}")
        print("-" * 50)
        result = ssh_tool.invoke({
            "command": cmd,
            # 环境变量中已经配置了这些值，所以不需要显式指定
            # "host": os.getenv("SSH_HOST"),
            # "username": os.getenv("SSH_USERNAME"),
            # "password": os.getenv("SSH_PASSWORD")
        })
        print(result)
        print("-" * 50)

if __name__ == "__main__":
    test_ssh_commands() 