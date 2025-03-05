from ActionNode import ActionNode
from SSHAction import SSHExecute
import asyncio

# 创建一个异步SSH命令执行函数
async def execute_ssh_command(host="172.16.100.2", port=22, username="root", command="docker ps"):
    ssh_action = SSHExecute()
    result = await ssh_action.run(
        host=host,
        port=port,
        username=username,
        command=command
    )
    return result

# 创建一个包装了SSH命令的ActionNode
def create_ssh_action_node(name, command):
    async def ssh_action():
        result = await execute_ssh_command(command=command)
        return result
    
    # 创建一个同步包装函数
    def sync_wrapper():
        return asyncio.run(ssh_action())
    
    return ActionNode(name, sync_wrapper)

# 使用示例
def main():
    # 创建一个执行 docker ps 命令的节点
    docker_ps_node = create_ssh_action_node("Docker PS", "docker ps")
    
    # 执行节点
    result = docker_ps_node.execute()
    print(f"执行结果:\n{result}")

if __name__ == "__main__":
    main()