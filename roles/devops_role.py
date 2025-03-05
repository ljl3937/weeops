# 原第2行修改
from metagpt.actions import Action, WriteCode
from metagpt.roles import Role
from metagpt.management.skill_manager import SkillManager
from metagpt.roles.role import RoleReactMode
from metagpt.utils.common import any_to_name
from metagpt.schema import Message
# 修改为绝对路径导入
from actions.SSHAction import SSHExecute