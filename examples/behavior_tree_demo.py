# behavior_tree_demo.py
# 使用ActionNode构建简单的行为树示例

from actions.ActionNode import ActionNode
from actions.SSHAction import SSHExecute
import asyncio

# 创建一个异步SSH命令执行函数
async def execute_ssh_command(host="100.2", port=22, username="root", command="ls"):
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

# 定义一个简单的顺序节点，按顺序执行所有子节点
class SequenceNode:
    def __init__(self, name, children=None):
        """
        初始化顺序节点
        :param name: 节点名称
        :param children: 子节点列表
        """
        self.name = name
        self.children = children or []
    
    def add_child(self, child):
        """
        添加子节点
        :param child: 要添加的子节点
        """
        self.children.append(child)
    
    def execute(self):
        """
        按顺序执行所有子节点，如果有一个失败则停止
        :return: 执行结果
        """
        print(f"执行顺序节点 {self.name}")
        results = []
        
        for child in self.children:
            print(f"执行子节点 {child.name}")
            result = child.execute()
            results.append(result)
            
            # 如果子节点执行失败，则整个顺序节点失败
            if not result:
                return False
        
        return results

# 使用示例
def main():
    # 创建几个SSH命令节点
    ls_node = create_ssh_action_node("列出文件", "ls -la")
    docker_ps_node = create_ssh_action_node("查看容器", "docker ps")
    disk_usage_node = create_ssh_action_node("查看磁盘使用", "df -h")
    
    # 创建一个顺序节点，将所有命令组合在一起
    deployment_sequence = SequenceNode("部署检查序列")
    deployment_sequence.add_child(ls_node)
    deployment_sequence.add_child(docker_ps_node)
    deployment_sequence.add_child(disk_usage_node)
    
    # 执行整个序列
    print("开始执行部署检查序列...\n")
    results = deployment_sequence.execute()
    
    print("\n部署检查序列执行完成!")
    if results:
        print("所有检查都成功完成")
    else:
        print("检查序列中有失败项")

if __name__ == "__main__":
    main()