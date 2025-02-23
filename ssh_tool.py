from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

class SSHCommandInput(BaseModel):
    """输入参数模型"""
    command: str = Field(..., description="要在远程服务器上执行的命令")
    host: str = Field(default_factory=lambda: os.getenv("SSH_HOST"), description="SSH 主机地址")
    username: str = Field(default_factory=lambda: os.getenv("SSH_USERNAME"), description="SSH 用户名")
    password: str = Field(default_factory=lambda: os.getenv("SSH_PASSWORD"), description="SSH 密码")
    port: int = Field(default=22, description="SSH 端口号")

class SSHTool(BaseTool):
    name: str = "ssh_tool"
    description: str = "在远程服务器执行SSH命令"
    args_schema: Type[BaseModel] = SSHCommandInput

    # 必须实现基类的抽象方法 _run（而不是 _execute）
    def _run(
        self,
        command: str,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        port: int = 22,
        **kwargs
    ) -> str:
        """实际执行SSH命令的方法"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=host or os.getenv("SSH_HOST"),
                username=username or os.getenv("SSH_USERNAME"),
                password=password or os.getenv("SSH_PASSWORD"),
                port=port
            )
            
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            ssh.close()
            
            return output if not error else f"错误: {error}"
            
        except Exception as e:
            return f"SSH连接失败: {str(e)}"

# 使用示例需要改为使用 _run 的调用方式
if __name__ == "__main__":
    ssh_tool = SSHTool()
    # 正确调用方式（使用工具的标准接口）
    result = ssh_tool.run({
        "command": "ls -la",
        "host": os.getenv("SSH_HOST"),
        "username": os.getenv("SSH_USERNAME"),
        "password": os.getenv("SSH_PASSWORD")
    })
    print(result) 