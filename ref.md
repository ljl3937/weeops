`ActionNode` 通常在行为树（Behavior Tree）相关的编程中使用。行为树是一种用于人工智能和游戏开发中管理和组织角色行为的结构。下面是一个简单的 Python 示例，演示如何使用 `ActionNode`：

```python
# 定义 ActionNode 类
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

# 定义一个具体的动作函数
def move_forward():
    print("向前移动")
    return True

# 创建一个 ActionNode 实例
move_forward_node = ActionNode("向前移动节点", move_forward)

# 执行 ActionNode
result = move_forward_node.execute()
print(f"动作执行结果: {result}")
```

在这个例子中，我们定义了一个 `ActionNode` 类，它有一个构造函数 `__init__` 用于初始化节点的名称和要执行的动作函数。`execute` 方法用于执行该动作函数。

然后我们定义了一个具体的动作函数 `move_forward`，它会打印出“向前移动”的信息并返回 `True`。

接着我们创建了一个 `ActionNode` 实例 `move_forward_node`，并调用其 `execute` 方法来执行该节点的动作，最后打印出动作执行的结果。
