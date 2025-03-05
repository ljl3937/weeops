from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.actions import Action
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import asyncio
# 导入 Environment 和 UserRequirement
from metagpt.environment import Environment
from metagpt.schema import UserRequirement
from environment.web.selenium_env import SeleniumEnv

# 定义百度搜索的动作
class BaiduSearchAction(Action):
    """执行百度搜索的动作"""
    name: str = "BaiduSearchAction"
    
    async def run(self, query: str) -> str:
        """执行百度搜索并返回结果"""
        try:
            # 获取环境实例
            selenium_env = self.context.env.get_env("selenium")
            
            # 使用环境导航到百度
            selenium_env.execute_selenium_action({"action_type": "NAVIGATE", "url": "https://www.baidu.com"})
            
            # 尝试使用LLM定位搜索框
            try:
                search_result = selenium_env.execute_selenium_action({
                    "action_type": "FIND_ELEMENT_WITH_LLM",
                    "user_intent": "搜索输入框"
                })
                search_box = search_result["element"]
            except Exception:
                # 如果LLM定位失败，使用传统方式定位
                search_box = selenium_env.execute_selenium_action({
                    "action_type": "FIND_ELEMENT", 
                    "by": By.ID, 
                    "value": "kw"
                })["element"]
            
            # 尝试使用LLM定位搜索按钮
            try:
                button_result = selenium_env.execute_selenium_action({
                    "action_type": "FIND_ELEMENT_WITH_LLM",
                    "user_intent": "搜索按钮"
                })
                search_button = button_result["element"]
            except Exception:
                # 如果LLM定位失败，使用传统方式定位
                search_button = selenium_env.execute_selenium_action({
                    "action_type": "FIND_ELEMENT", 
                    "by": By.ID, 
                    "value": "su"
                })["element"]
            
            # 输入搜索内容
            selenium_env.execute_selenium_action({"action_type": "SEND_KEYS", "element": search_box, "keys": query})
            
            # 点击搜索按钮
            selenium_env.execute_selenium_action({"action_type": "CLICK_ELEMENT", "element": search_button})
            
            # 等待页面加载
            time.sleep(3)
            
            # 获取搜索结果页面的标题
            result_title = selenium_env.execute_selenium_action({"action_type": "GET_TITLE"})
            
            return f"搜索结果标题: {result_title}"
        except Exception as e:
            return f"搜索过程中发生错误: {str(e)}"
        finally:
            # 关闭浏览器
            try:
                selenium_env.execute_selenium_action({"action_type": "QUIT"})
            except:
                pass

# 定义百度搜索角色
class BaiduSearchRole(Role):
    """执行百度搜索的角色"""
    
    def __init__(self, name="BaiduSearcher", profile="Baidu Searcher", goal="Search information on Baidu", **kwargs):
        super().__init__(name=name, profile=profile, goal=goal, **kwargs)
        # 设置动作
        self.set_actions([BaiduSearchAction])
        # 监听用户需求消息
        self._watch([UserRequirement])
    
    async def _act(self) -> Message:
        """执行搜索动作"""
        # 获取最新的消息作为搜索查询
        latest_msg = self.get_memories(k=1)[0]
        query = latest_msg.content
        
        # 执行搜索动作
        todo = self.rc.todo
        result = await todo.run(query)
        
        # 返回搜索结果消息
        return Message(content=result, role=self.profile, cause_by=type(todo))

# 主函数
async def main():
    # 创建环境
    env = Environment()
    
    # 创建并添加 SeleniumEnv 到环境
    selenium_env = SeleniumEnv()
    # 将selenium环境添加到主环境中
    env.envs["selenium"] = selenium_env
    
    # 创建百度搜索角色并添加到环境
    searcher = BaiduSearchRole(context=env.context)
    env.add_role(searcher)
    
    # 定义搜索查询内容
    query = "人工智能的发展趋势"
    print(f"开始搜索: {query}")
    
    # 发布用户需求消息
    user_msg = Message(content=query, role="User", cause_by=UserRequirement)
    env.publish_message(user_msg)
    
    # 运行环境直到所有任务完成
    await env.run()
    
    print("搜索任务已完成")

if __name__ == "__main__":
    asyncio.run(main())