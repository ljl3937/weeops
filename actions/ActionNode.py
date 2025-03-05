# ActionNode.py
# 基于ref.md中的示例实现ActionNode类

class ActionNode:
    def __init__(self, name, action):
        """
        初始化 ActionNode
        :param name: 节点的名称
        :param action: 节点要执行的动作函数
        """
        self.name = name
        self.action = action

    def execute(self):
        """
        执行节点的动作
        :return: 动作执行的结果
        """
        print(f"执行 {self.name} 节点的动作")
        return self.action()