# test_selenium.py
import unittest
from environment.web.selenium_env import SeleniumEnv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSeleniumEnv(unittest.TestCase):
    def setUp(self):
        self.env = SeleniumEnv()

    def tearDown(self):
        self.env.execute_selenium_action({"action_type": "QUIT"})

    # def test_navigate(self):
    #     """测试导航到百度首页"""
    #     action = {"action_type": "NAVIGATE", "url": "https://www.baidu.com"}
    #     _, _, _, _, result = self.env.step(action)
    #     self.assertEqual(result["res"]["url"], "https://www.baidu.com/")

    # def test_find_element(self):
    #     """测试查找百度首页的搜索框"""
    #     # 导航到百度首页
    #     self.env.execute_selenium_action({"action_type": "NAVIGATE", "url": "https://www.baidu.com"})
        
    #     # 查找搜索框元素（通过 ID 定位）
    #     action = {"action_type": "FIND_ELEMENT", "by": By.ID, "value": "kw"}
    #     _, _, _, _, result = self.env.step(action)
    #     self.assertIsNotNone(result["res"]["element"])

    # def test_click_element(self):
    #     """测试点击百度首页的“百度一下”按钮"""
    #     # 导航到百度首页
    #     self.env.execute_selenium_action({"action_type": "NAVIGATE", "url": "https://www.baidu.com"})
        
    #     # 查找“百度一下”按钮（通过 ID 定位）
    #     find_action = {"action_type": "FIND_ELEMENT", "by": By.ID, "value": "su"}
    #     _, _, _, _, find_result = self.env.step(find_action)
    #     element = find_result["res"]["element"]
        
    #     # 点击按钮
    #     click_action = {"action_type": "CLICK_ELEMENT", "element": element}
    #     _, _, _, _, click_result = self.env.step(click_action)
    #     self.assertIsNotNone(click_result["res"])

    # def test_send_keys(self):
    #     """测试向百度搜索框输入文本"""
    #     # 导航到百度首页
    #     self.env.execute_selenium_action({"action_type": "NAVIGATE", "url": "https://www.baidu.com"})
        
    #     # 查找搜索框元素（通过 ID 定位）
    #     find_action = {"action_type": "FIND_ELEMENT", "by": By.ID, "value": "kw"}
    #     _, _, _, _, find_result = self.env.step(find_action)
    #     element = find_result["res"]["element"]
        
    #     # 向搜索框输入文本
    #     send_keys_action = {"action_type": "SEND_KEYS", "element": element, "keys": "Hello, Selenium!"}
    #     _, _, _, _, send_keys_result = self.env.step(send_keys_action)
    #     self.assertIsNotNone(send_keys_result["res"])

    def test_submit_search(self):
        """测试提交搜索并验证结果页标题"""
        # 导航到百度首页
        self.env.execute_selenium_action({"action_type": "NAVIGATE", "url": "https://www.baidu.com"})
        
        # 查找搜索框元素并输入文本
        find_action = {"action_type": "FIND_ELEMENT", "by": By.ID, "value": "kw"}
        _, _, _, _, find_result = self.env.step(find_action)
        element = find_result["res"]["element"]
        
        send_keys_action = {"action_type": "SEND_KEYS", "element": element, "keys": "Selenium 测试"}
        self.env.step(send_keys_action)
        
        # 模拟按下回车键提交搜索
        submit_action = {"action_type": "SEND_KEYS", "element": element, "keys": Keys.RETURN}
        self.env.step(submit_action)
        
        # 提交搜索后等待页面加载完成
        WebDriverWait(self.env.driver, 10).until(
            EC.presence_of_element_located((By.ID, "content_left"))
        )

        # 验证结果页标题是否包含搜索关键词
        title_action = {"action_type": "GET_TITLE"}
        _, _, _, _, title_result = self.env.step(title_action)
        print(f"Page title: {title_result['res']}")
        self.assertIn("Selenium 测试", title_result["res"])

if __name__ == "__main__":
    unittest.main()