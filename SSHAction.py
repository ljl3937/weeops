# 步骤1：创建SSH Action
from metagpt.actions import Action
import asyncssh
from metagpt.management.skill_manager import SkillManager
from metagpt.roles import Role
from metagpt.actions import WriteCode
from metagpt.roles.role import RoleReactMode
from metagpt.utils.common import any_to_name
from metagpt.schema import Message  # 引入 Message 类

# 修改后的SSHExecute类（添加username参数）
class SSHExecute(Action):
    async def run(self, host: str, port: int, username: str, command: str):  # 添加username参数
        """SSH连接执行命令
        :param host: 目标主机IP
        :param port: SSH端口（建议改为int类型）
        :param username: 登录用户名
        :param command: 要执行的命令
        """
        async with asyncssh.connect(
            host=host,
            port=port,
            username=username,  # 新增用户名配置
            # 注意：这里需要添加认证方式（密码/密钥）
            # password='your_password',  # 不推荐明文密码
            client_keys=['/home/jialin/.ssh/id_ed25519']  # 推荐使用密钥认证
        ) as conn:
            return await conn.run(command)

# # 步骤2：添加到工具链
# skill_manager = SkillManager()
# ssh_execute = SSHExecute(name="SSHExecute")
# ssh_execute.desc = "用来执行远程服务器的命令"
# skill_manager.add_skill(ssh_execute)

# 步骤3：在Role中使用
class DevOpsEngineer(Role):
    name: str = "东东"
    profile: str = "Automation Specialist"
    goals: list[str] = ["Automate deployment processes"]
    constraints: str = "Must use secure SSH connections"
    todo_action: str = ""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([SSHExecute, WriteCode])
        self.rc.react_mode = RoleReactMode.BY_ORDER
        self.todo_action = any_to_name(SSHExecute)
        
    # 添加重写 act 方法接收命令参数
    async def act(self, command: str = None) -> Message:
        """重写 act 方法以接收命令参数"""
        if command:
            return await self._act(command)
        else:
            # 默认行为，调用父类的 act 方法
            return await super().act()
        
    # 可在DevOpsEngineer类中添加结果处理方法
    def _handle_result(self, result):
        if result.exit_status != 0:
            print(f"命令执行失败！错误信息：{result.stderr}")
        else:
            print(f"命令执行成功：\n{result.stdout}")
            
    async def _act(self, command: str):
        # 修复：直接创建并调用 SSHExecute，而不是使用 self.rc.todo
        ssh_action = SSHExecute()
        result = await ssh_action.run(
            host="100.2",
            port=22,
            username="root",
            command=command
        )
        # 修复：直接返回结果或使用 Message 类包装
        
        self._handle_result(result)
        return Message(content=str(result))